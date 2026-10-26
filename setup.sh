#!/usr/bin/env bash
# Fault-Detect: set up the whole project.
# Run it from anywhere inside the project (in VS Code: Terminal > New Terminal, choose Git Bash):
#     bash setup.sh      (or  bash ../setup.sh  if you are in a sub-folder)
# It makes two folders: backend (Flask) and frontend (React), with a starter file for every part.
# Safe to run again: it never overwrites a file that already exists, except the Vite config.
set -e

# Always work in the folder this script sits in, wherever it was started from.
cd "$(dirname "$0")"

# Find a Python that really runs. On Windows, "python3" can be a Microsoft Store shortcut that does nothing.
PY=""
for c in python py python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" --version >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "Python is not installed (or only the Microsoft Store shortcut is there)."
  echo "Install Python 3.11 or newer from python.org and tick 'Add Python to PATH'."
  echo "Then close VS Code, open it again, and run this again."
  exit 1
fi
echo "Using Python: $PY"
command -v node >/dev/null || { echo "Node.js is not installed. Install Node 20 or newer, then run this again."; exit 1; }

# write a file only if it is not there yet
put() { if [ -e "$1" ]; then echo "  kept   $1"; cat > /dev/null; else mkdir -p "$(dirname "$1")"; cat > "$1"; echo "  made   $1"; fi; }

echo "== Backend (Flask) =="
mkdir -p backend
cd backend

put requirements.txt <<'EOF'
flask
flask-cors
flask-socketio
simple-websocket
python-dotenv
bcrypt
numpy
scikit-learn
psycopg2-binary
EOF

put .env.example <<'EOF'
# Copy this file to .env and fill it in.
# Leave DATABASE_URL empty to use a second local file as the "online" database (simulated).
DATABASE_URL=
# The size of the local storage file, in megabytes. This is the "set storage" for FR-21a.
LOCAL_STORAGE_CAP_MB=512
EOF

put config.py <<'EOF'
"""Every setting in one place. The numbers come from the SRS. Change them here only."""
import os
from dotenv import load_dotenv

load_dotenv()

READING_INTERVAL_S = 1         # FR-3a   one reading per second per parameter
WINDOW_S = 10                  # FR-6, PR-001   status is set every 10 seconds
SENSOR_TIMEOUT_S = 3           # FR-13   no reading for 3 seconds = sensor fault
ALERT_LIMIT_S = 2              # PR-001a, PR-001b, PR-002
NORMAL_KEEP_HOURS = 24         # FR-9b   readings of a normal window are deleted after this
STORAGE_ALERT_AT = 0.75        # FR-21a, NFR-10
LOCAL_STORAGE_CAP_MB = int(os.getenv("LOCAL_STORAGE_CAP_MB", "512"))  # placeholder: measure, then decide
LOCAL_DB_PATH = os.getenv("LOCAL_DB_PATH", "local_store.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")
ONLINE_FALLBACK_PATH = "online_store.db"   # used when DATABASE_URL is empty (simulated online database)

SESSION_DEFAULT_MIN = 5        # FR-26
SESSION_MIN_MIN = 1
SESSION_MAX_MIN = 5
LOGIN_MAX_FAILS = 5            # FR-28d
LOGIN_BLOCK_MIN = 15
PASSWORD_MIN_LEN = 15          # FR-28a
PASSWORD_MAX_LEN = 128         # must accept 64 or more

# Limits from Appendix A. None means the SRS gives no number: the team has to decide (see build-plan).
# "warning" and "critical" are levels. "abnormal" is for parameters that only have one abnormal level (FR-5).
LIMITS = {
    "motor": {
        "temperature": {"warning": 130, "critical": 150},
        "current":     {"warning": 31,  "critical": 35},
        "vibration":   {"warning": None, "critical": None},   # SRS: normal below 2.8 mm/s, critical "per ISO 10816-3"
        "rpm":         {"warning": None, "critical": None},
    },
    "pump": {
        "temperature": {"abnormal": 95},                      # bearing temperature
        "current":     {"abnormal": None},
        "vibration":   {"abnormal": 5.0},
        "rpm":         {"abnormal": None},
    },
    "ups": {
        "temperature": {"abnormal": 75},                      # internal temperature
        "current":     {"abnormal": None},
        "fan_rpm":     {"abnormal_below": 1000},
    },
}

# What counts as a physically possible reading (FR-14). These are placeholders for the team to confirm.
PHYSICAL_RANGE = {
    "temperature": (-20, 300),
    "current": (0, 500),
    "vibration": (0, 100),
    "rpm": (0, 10000),
    "fan_rpm": (0, 10000),
}
EOF

put checker.py <<'EOF'
"""The checker. Every reading passes through here before the status model. FR-14, NFR-7."""
from config import PHYSICAL_RANGE


def check_reading(reading):
    """Return (True, "") if the reading is clean, otherwise (False, reason).

    A reading is a dict: {"machine_id", "parameter", "value", "time"}.
    A bad reading is kept out, logged as invalid, and the system carries on.
    """
    value = reading.get("value")
    if value is None:
        return False, "missing"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False, "wrong type"
    if value != value:
        return False, "not a number"
    low, high = PHYSICAL_RANGE.get(reading.get("parameter"), (None, None))
    if low is not None and not (low <= value <= high):
        return False, "impossible value"
    return True, ""
EOF

put model.py <<'EOF'
"""The status model. Threshold screening, then the 10-second trend check, then the classifier.
FR-4, FR-5, FR-6, NFR-1, NFR-2, NFR-9. One parameter's logic can change without touching the others."""
from config import LIMITS


def threshold_level(machine_type, parameter, value):
    """Return "normal", "warning", "critical" or "abnormal" for ONE reading. FR-4."""
    rule = LIMITS.get(machine_type, {}).get(parameter, {})
    if rule.get("critical") is not None and value > rule["critical"]:
        return "critical"
    if rule.get("warning") is not None and value > rule["warning"]:
        return "warning"
    if rule.get("abnormal") is not None and value > rule["abnormal"]:
        return "abnormal"
    if rule.get("abnormal_below") is not None and value < rule["abnormal_below"]:
        return "abnormal"
    return "normal"


def trend_check(levels):
    """levels = the threshold level of each clean reading in the 10-second window.
    A fault needs the abnormal condition to hold across the window, never one reading alone. FR-6."""
    if not levels:
        return "normal"
    # TODO step 4: decide how much of the window must be abnormal. Starting rule: all of it.
    order = ["normal", "abnormal", "warning", "critical"]
    worst_common = min(levels, key=order.index)
    return worst_common


def classify(machine_type, parameter, window_values):
    """The classifier sets the final status for the window. FR-5.
    TODO step 10: train a logistic regression on the labelled simulated set (SRS Appendix D, NFR-1, NFR-2)."""
    levels = [threshold_level(machine_type, parameter, v) for v in window_values]
    return trend_check(levels)
EOF

put engine.py <<'EOF'
"""The engine. A reading splits into two streams the moment it arrives. See docs/design/engine.md.

  Stream 1: straight to the dashboard (every reading, even a wrong one).
  Stream 2: checker -> status model (10-second window) -> status -> save to both stores.
"""
import time
from config import WINDOW_S, SENSOR_TIMEOUT_S
from checker import check_reading


class Engine:
    def __init__(self, send_live, send_status, save_window):
        self.send_live = send_live        # called with every reading (stream 1)
        self.send_status = send_status    # called with each new status
        self.save_window = save_window    # called after every 10-second window
        self.buffer = {}                  # (machine_id, parameter) -> clean readings of this window
        self.last_seen = {}               # (machine_id, parameter) -> time of last reading (FR-13)
        self.window_started = time.time()

    def handle_reading(self, reading):
        key = (reading["machine_id"], reading["parameter"])
        self.last_seen[key] = time.time()
        ok, reason = check_reading(reading)
        self.send_live({**reading, "valid": ok, "reason": reason})     # stream 1
        if not ok:
            return                                                      # kept out of the model, logged (FR-14)
        self.buffer.setdefault(key, []).append(reading["value"])        # stream 2
        if time.time() - self.window_started >= WINDOW_S:
            self.close_window()

    def silent_sensors(self):
        """Parameters with no reading for SENSOR_TIMEOUT_S seconds. FR-13."""
        now = time.time()
        return [k for k, t in self.last_seen.items() if now - t >= SENSOR_TIMEOUT_S]

    def close_window(self):
        # TODO step 4: run model.classify for each key, send_status, then save_window. Step 5: raise faults.
        self.buffer = {}
        self.window_started = time.time()
EOF

put faults.py <<'EOF'
"""Fault records and their life. Open -> acknowledged (each person for themselves) -> resolved. Step 5.

FR-7, FR-7a, FR-7b, FR-7c   pop-up to every connected Operator and Engineer; never to the Administrator
FR-8, FR-8a, FR-8b          each person acknowledges for themselves; record who and when; acknowledging does not close it
FR-15                       one fault record per abnormal parameter
FR-16                       no duplicate alert while a fault is open
FR-17                       only an Engineer resolves, after acknowledging; record when
FR-18, FR-19                maintenance mode for a stated time; alerts pause; overdue flag
FR-23d                      each fault stores the limit in force when it was raised
"""


def raise_fault(machine_id, parameter, level, limit_in_force):
    raise NotImplementedError("step 5")


def acknowledge(fault_id, user):
    raise NotImplementedError("step 5")


def resolve(fault_id, engineer):
    raise NotImplementedError("step 5")


def set_maintenance(machine_id, minutes, engineer):
    raise NotImplementedError("step 8")
EOF

put storage.py <<'EOF'
"""Two stores, written at the same time. Step 6.

  Local storage: a SQLite file with a set size (LOCAL_STORAGE_CAP_MB). When it is full, writes fail for real.
  Online database: PostgreSQL if DATABASE_URL is set; otherwise a second SQLite file stands in for it.

FR-9, FR-9a, FR-9b, FR-12, FR-20, FR-21, FR-21a, NFR-6, NFR-10, PR-006
"""
import json
import sqlite3
from config import LOCAL_DB_PATH, LOCAL_STORAGE_CAP_MB, ONLINE_FALLBACK_PATH, STORAGE_ALERT_AT

PAGE = 4096
SCHEMA = """CREATE TABLE IF NOT EXISTS windows (
    machine_id TEXT, parameter TEXT, start_time REAL, status TEXT, readings TEXT)"""


class LocalStore:
    def __init__(self, path=LOCAL_DB_PATH, cap_mb=LOCAL_STORAGE_CAP_MB):
        self.cap_pages = cap_mb * 1024 * 1024 // PAGE
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.execute(f"PRAGMA page_size={PAGE}")
        self.con.execute(f"PRAGMA max_page_count={self.cap_pages}")   # the set size: the file cannot grow past it
        self.con.execute(SCHEMA)
        self.con.commit()

    def used_fraction(self):
        """Used space as a share of the set size. Free pages inside the file do not count. FR-21a."""
        pages = self.con.execute("PRAGMA page_count").fetchone()[0]
        free = self.con.execute("PRAGMA freelist_count").fetchone()[0]
        return (pages - free) / self.cap_pages

    def at_alert_level(self):
        return self.used_fraction() >= STORAGE_ALERT_AT

    def save_window(self, window):
        """Return True if saved, False if the store is full. The caller logs it and keeps the data. FR-20."""
        try:
            self.con.execute("INSERT INTO windows VALUES (?,?,?,?,?)",
                             (window["machine_id"], window["parameter"], window["start_time"],
                              window["status"], json.dumps(window.get("readings", []))))
            self.con.commit()
            return True
        except sqlite3.OperationalError:
            return False


class OnlineStore:
    """PostgreSQL when DATABASE_URL is set. The demo can cut the link with set_available(False). FR-12."""
    def __init__(self):
        self.available = True
        self.con = sqlite3.connect(ONLINE_FALLBACK_PATH, check_same_thread=False)   # TODO step 6: PostgreSQL
        self.con.execute(SCHEMA)
        self.con.commit()

    def set_available(self, value):
        self.available = value

    def save_window(self, window):
        if not self.available:
            return False
        self.con.execute("INSERT INTO windows VALUES (?,?,?,?,?)",
                         (window["machine_id"], window["parameter"], window["start_time"],
                          window["status"], json.dumps(window.get("readings", []))))
        self.con.commit()
        return True


def delete_old_normal_readings():
    """FR-9b: readings of normal windows go after 24 hours. Statuses and warning or critical records stay."""
    raise NotImplementedError("step 6")
EOF

put auth.py <<'EOF'
"""Sign in, passwords, roles. Step 7.
FR-26 sign-out time (1 to 5 minutes, each person's own), FR-27 Administrator-only functions, FR-28 sign in first,
FR-28a long passwords, FR-28b no forced mix or schedule, FR-28c refuse common passwords, FR-28d lockout,
FR-28e secure connection (set up when the server starts), FR-28f salted, scrambled passwords."""
import pathlib
import bcrypt
from config import PASSWORD_MIN_LEN, PASSWORD_MAX_LEN

ROLES = ("operator", "engineer", "administrator")
_COMMON = set()
_p = pathlib.Path(__file__).with_name("common-passwords.txt")
if _p.exists():
    _COMMON = {line.strip().lower() for line in _p.read_text(encoding="utf-8").splitlines() if line.strip()}


def password_problem(password):
    """Return a plain message if the password is not allowed, else None."""
    if len(password) < PASSWORD_MIN_LEN:
        return f"Use at least {PASSWORD_MIN_LEN} characters."
    if len(password) > PASSWORD_MAX_LEN:
        return f"Use at most {PASSWORD_MAX_LEN} characters."
    if password.lower() in _COMMON:
        return "That password is too common."
    return None     # no rule about capitals, numbers or symbols (FR-28b)


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)
EOF

put common-passwords.txt <<'EOF'
password1234567
123456789012345
qwertyuiopasdfg
iloveyou1234567
administrator123
EOF

put admin.py <<'EOF'
"""Administrator and limits. Step 7.
FR-22 change log (who and when), FR-23 keep the old limit and date, FR-23a Engineer changes limits without a restart,
FR-23b reject a warning limit that is not below the critical limit, FR-23c a new limit applies to later readings,
FR-27 only the Administrator manages users and machines. The Administrator cannot reset passwords."""


def change_limit(machine_type, parameter, warning, critical, engineer):
    if warning is not None and critical is not None and warning >= critical:
        return False, "The warning limit must be below the critical limit."     # FR-23b
    raise NotImplementedError("step 7")
EOF

put reports.py <<'EOF'
"""History and reports. Step 8.
FR-9 call up faults and readings, FR-10 everyone views fault history; Operators and Engineers make reports
for a day, week, month or year (full readings only where kept, FR-9b)."""


def report(machine_id, period):
    raise NotImplementedError("step 8")
EOF

put seed.py <<'EOF'
"""Seed data. All sensor readings, and every injection, come from here. Step 2.
FR-1, FR-2, FR-3, FR-24: machines and their parameters. FR-3a: one reading per second."""
import random
import time

PARAMETERS = {
    "motor": ["temperature", "current", "vibration", "rpm"],
    "pump": ["temperature", "current", "vibration", "rpm"],     # temperature = bearing temperature
    "ups": ["temperature", "current", "fan_rpm"],               # temperature = internal temperature
}

# Starting values for normal running. Adjust them when the screens exist.
NORMAL = {
    "motor": {"temperature": 90, "current": 28, "vibration": 1.8, "rpm": 1480},
    "pump": {"temperature": 65, "current": 12, "vibration": 2.0, "rpm": 1450},
    "ups": {"temperature": 50, "current": 5, "fan_rpm": 2500},
}

DEMO_MACHINES = [
    {"id": "motor-1", "name": "Motor 1", "type": "motor"},
    {"id": "motor-2", "name": "Motor 2", "type": "motor"},
    {"id": "motor-3", "name": "Motor 3", "type": "motor"},
    {"id": "pump-1", "name": "Pump 1", "type": "pump"},
    {"id": "ups-1", "name": "UPS 1", "type": "ups"},
]


def make_machines(count):
    """For the heavy-load test (PR-003): 10 or more machines across the three types."""
    kinds = ["motor", "pump", "ups"]
    return [{"id": f"{kinds[i % 3]}-{i + 1}", "name": f"{kinds[i % 3].title()} {i + 1}", "type": kinds[i % 3]}
            for i in range(count)]


def normal_reading(machine, parameter):
    base = NORMAL[machine["type"]][parameter]
    return {"machine_id": machine["id"], "parameter": parameter,
            "value": round(random.gauss(base, base * 0.01), 2), "time": time.time()}
EOF

put demo.py <<'EOF'
"""The demo control panel. Step 9. FR-11 near and remote mode, FR-12 cut and restore the connection, DC-006.
Each scenario is seed data played in order. The list matches docs/design/test-plan.md."""

SCENARIOS = [
    "Normal running", "Lone spike", "Sustained warning", "Sustained critical", "Two faults at once",
    "Sensor goes silent", "Bad reading", "Connection cut", "Storage fills up", "Storage fails", "Restart",
    "Maintenance", "Fault returns", "Limit change", "Nobody connected", "Noisy readings", "Heavy load",
    "Slow alert", "Labelled test set", "Login checks", "Near and remote mode", "Old data",
]


def play(name):
    raise NotImplementedError("step 9")
EOF

put metrics.py <<'EOF'
"""Numbers for the 'measure' tests. Step 10.
NFR-5 uptime, PR-001 status update time, PR-001a alert time, PR-002 dashboard time,
PR-003 10 machines, PR-004 5 users, PR-005 40 readings per second, PR-007 start-up within 60 seconds."""
import time

STARTED = time.time()


def uptime_seconds():
    return time.time() - STARTED
EOF

put app.py <<'EOF'
"""The Flask server. Run it with:  python app.py"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from seed import DEMO_MACHINES, PARAMETERS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


@app.get("/api/machines")
def machines():
    return jsonify([{**m, "parameters": PARAMETERS[m["type"]]} for m in DEMO_MACHINES])


if __name__ == "__main__":
    # FR-28e: for https, give the server a certificate (see SETUP.md, "Secure connection").
    socketio.run(app, host="127.0.0.1", port=5000, allow_unsafe_werkzeug=True)
EOF

echo "  making the Python environment (this takes a minute)"
if [ ! -d venv ]; then "$PY" -m venv venv; fi
if [ -x venv/Scripts/pip ] || [ -x venv/Scripts/pip.exe ]; then PIP=venv/Scripts/pip; else PIP=venv/bin/pip; fi
$PIP install -q -r requirements.txt
cd ..

echo "== Frontend (React) =="
if [ ! -d frontend ]; then
  npm create vite@latest frontend -- --template react < /dev/null
fi
cd frontend
npm install
npm install react-router-dom socket.io-client recharts
rm -f src/App.css src/index.css

cat > vite.config.js <<'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Sends /api and the live connection to the Flask server on port 5000.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000',
      '/socket.io': { target: 'http://127.0.0.1:5000', ws: true },
    },
  },
})
EOF

put src/theme.css <<'EOF'
:root {
  /* Canvas & surfaces - diary/paper feel */
  --bg-canvas:      #dbdee0;
  --bg-card:        #F8F9FB;
  --bg-sidebar:     #2B3A4A;
  --bg-sidebar-hover: #344657;
  --bg-chart:       #F1F4F8;

  /* Brand colors - muted yacht blue palette + Gold */
  --primary:        #2C3A4C;
  --primary-dim:    rgba(44, 58, 76, 0.08);
  --secondary:      #5B7C99;
  --secondary-dim:  rgba(91, 124, 153, 0.08);
  --gold:           #C4A35A;
  --gold-dim:       rgba(196, 163, 90, 0.1);
  --warning:        #B8A06A;
  --warning-dim:    rgba(184, 160, 106, 0.1);
  --teal:           #6B8E7B;
  --teal-dim:       rgba(107, 142, 123, 0.08);
  --red:            #A06B6B;
  --red-dim:        rgba(160, 107, 107, 0.1);
  --purple:         #7B6B8E;
  --purple-dim:     rgba(123, 107, 142, 0.1);

  /* Text hierarchy */
  --text-head:      #2D3748;
  --text-body:      #4A5568;
  --text-muted:     #8B9BB0;

  /* Borders */
  --border-faint:   #E5E8ED;
  --border-light:   #D5DAE1;
}

/* TODO: dark theme colours are not chosen yet. When they are, put them here:
:root[data-theme="dark"] { ... } */

* { box-sizing: border-box; }
body { margin: 0; background: var(--bg-canvas); color: var(--text-body);
       font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }
h1, h2, h3 { color: var(--text-head); }
.page { padding: 24px; max-width: 1200px; margin: 0 auto; }
.card { background: var(--bg-card); border: 1px solid var(--border-light); border-radius: 14px; padding: 16px; }
.muted { color: var(--text-body); font-size: 14px; }
.topbar { display: flex; align-items: center; gap: 16px; padding: 12px 24px; background: var(--bg-sidebar); color: #F8F9FB; }
.topbar input { flex: 1; max-width: 360px; padding: 8px 12px; border-radius: 8px; border: 1px solid var(--border-light); }
.topbar button { background: transparent; color: #F8F9FB; border: 1px solid var(--bg-sidebar-hover); border-radius: 8px; padding: 8px 12px; cursor: pointer; }
.brand { font-weight: 700; color: var(--gold); text-decoration: none; }
EOF

# main.jsx from the template is replaced on purpose, because it needs the router
cat > src/main.jsx <<'EOF'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './theme.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
EOF

cat > src/App.jsx <<'EOF'
import { Routes, Route, useLocation } from 'react-router-dom'
import TopBar from './TopBar.jsx'
import SignIn from './SignIn.jsx'
import Overview from './Overview.jsx'
import MachinesList from './MachinesList.jsx'
import MachineDetail from './MachineDetail.jsx'
import Settings from './Settings.jsx'
import Admin from './Admin.jsx'
import DemoPanel from './DemoPanel.jsx'
import Tracker from './Tracker.jsx'

export default function App() {
  const onSignIn = useLocation().pathname === '/signin'
  return (
    <>
      {!onSignIn && <TopBar />}
      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route path="/" element={<Overview />} />
        <Route path="/machines" element={<MachinesList />} />
        <Route path="/machine/:id" element={<MachineDetail />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/demo" element={<DemoPanel />} />
        <Route path="/tracker" element={<Tracker />} />
      </Routes>
    </>
  )
}
EOF

put src/api.js <<'EOF'
// Talks to the Flask server. The live connection carries the readings (stream 1) and the statuses.
import { io } from 'socket.io-client'

export async function get(path) {
  const r = await fetch(path)
  return r.json()
}

export async function post(path, body) {
  const r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  return r.json()
}

export const live = io({ autoConnect: false })
EOF

# one starter file per page or part: name, title, step, requirements
part() {
  put "src/$1.jsx" <<EOF
// $2
// Built in step $3. Requirements: $4
export default function $1() {
  return (
    <div className="page">
      <h1>$2</h1>
      <p className="muted">Starter file. Step $3. Requirements: $4</p>
    </div>
  )
}
EOF
}
part SignIn "Fault-Detect" 7 "FR-26, FR-28, FR-28a, FR-28b, FR-28c, FR-28d"
part Overview "Overview" 2 "FR-1, FR-2, FR-3, FR-13, FR-14, FR-24, NFR-8, PR-001, PR-002"
part MachinesList "Machines" 2 "FR-24, FR-5, FR-18"
part MachineDetail "Machine detail" 8 "FR-9, FR-10, FR-15, FR-17, FR-18, FR-19"
part Settings "Settings" 7 "FR-23, FR-23a, FR-23b, FR-26 (and the theme, see srs-changes)"
part Admin "Admin" 7 "FR-21a, FR-22, FR-27"
part DemoPanel "Demo control panel" 9 "FR-11, FR-12, DC-006"
part Tracker "Requirements tracker" 9 "every requirement"
part FaultPopup "Fault pop-up" 5 "FR-7, FR-7a, FR-7b, FR-7c, FR-8, FR-8a, FR-16"
part BellList "Bell list" 5 "FR-8b, FR-17"
part MachineCard "Machine card" 2 "FR-1, FR-2, FR-3, FR-5, FR-13, FR-14, FR-18, FR-19"

put src/TopBar.jsx <<'EOF'
import { Link } from 'react-router-dom'

// Shared top bar: name, search, bell, person. Step 5. See docs/design/top-bar.md
export default function TopBar() {
  return (
    <div className="topbar">
      <Link to="/" className="brand">Fault-Detect</Link>
      <input placeholder="Search machines" />
      <button>Bell</button>
      <button>Name</button>
    </div>
  )
}
EOF

cd ..
echo "== .gitignore =="
for line in "backend/venv/" "backend/__pycache__/" "backend/*.db" "backend/.env" "frontend/node_modules/" "frontend/dist/" ".obsidian/"; do
  grep -qxF "$line" .gitignore 2>/dev/null || echo "$line" >> .gitignore
done

echo
echo "Done. To run it, open two terminals:"
echo "  1)  cd backend && source venv/Scripts/activate && python app.py      (on Mac or Linux: source venv/bin/activate)"
echo "  2)  cd frontend && npm run dev"
echo "Then open http://localhost:5173 in the browser."