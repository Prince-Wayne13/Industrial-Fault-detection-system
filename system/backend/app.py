"""The Flask server. Run it with:  python app.py   (from system/backend)

Segment 2: the engine runs on simulated sensors in real time. Every reading goes straight to the screens over the live
connection ('reading'), every status goes out the moment its window closes ('status'), and a full snapshot goes out each
second ('overview'). Statuses and faults are saved to both stores by the engine itself.
Segment 3: faults, acknowledge, resolve, maintenance, history, report.
Segment 4: sign-in with a token, roles enforced here (not only on screen), settings, limits, admin.
Segment 5: demo control, requirements tracker, measured numbers, HTTPS."""
import base64
import copy
import os

import clock

_BOOT = clock.real()                                      # PR-007: start-up time is measured from here
from functools import wraps

from flask import Flask, Response, g, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import config
import proof
import reports
from auth import User, can
from live import LiveFeed
from seed import LIVE_MACHINES, PARAMETERS
from storage import DualStore, LocalStore, OnlineStore
from system import DEMO_USERS, System

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

clock.use_real()
system = System(machines=copy.deepcopy(LIVE_MACHINES), store=DualStore(LocalStore(), OnlineStore()), restarted=True)     # FR-21: carries on with the saved settings and faults
feed = LiveFeed(system,
                emit_reading=lambda r: socketio.emit("reading", r),
                emit_status=lambda w: socketio.emit("status", w),
                emit_overview=lambda o: socketio.emit("overview", o))
feed.started = _BOOT
viewers = set()
peak = {"viewers": 0}

_persist = system.faults.persist                         # tell every screen when a fault is raised, acknowledged or resolved


def _persist_and_tell(fault):
    _persist(fault)
    socketio.emit("faults_changed")


system.faults.persist = _persist_and_tell


# ---- accounts live in the database (the local store's settings), so they survive a restart ----
def save_accounts():
    system.store.local.put_setting("users", [
        {"username": u.username, "full_name": u.full_name, "role": u.role, "session_min": u.session_min,
         "pw_hash": base64.b64encode(u.pw_hash).decode()} for u in system.accounts.users.values()])


def load_accounts():
    rows = system.store.local.get_setting("users")
    if rows:
        system.accounts.users.clear()
        for r in rows:
            system.accounts.users[r["username"]] = User(r["username"], r["full_name"], r["role"], base64.b64decode(r["pw_hash"]), r["session_min"])
        system.users.clear()
        for key, (uname, _, _) in DEMO_USERS.items():
            if uname in system.accounts.users:
                system.users[key] = system.accounts.users[uname]
    else:
        save_accounts()


load_accounts()


# ---- who is calling ----
def _token():
    h = request.headers.get("Authorization", "")
    return h[7:] if h.startswith("Bearer ") else ""


def authed(action=None, touch=False):
    """FR-28: sign in first. FR-27: the role is checked here. touch=True means this call is a person's own action, so it keeps
    the session alive (FR-26); calls the screen makes by itself do not."""
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **k):
            with feed.lock:
                session = system.accounts.session_for(_token(), touch)
                user = system.accounts.users.get(session.username) if session else None
            if user is None:
                return jsonify({"ok": False, "message": "Sign in first."}), 401
            if action and not can(user.role, action):
                return jsonify({"ok": False, "message": "Your role cannot do that."}), 403
            g.user = user
            return fn(*a, **k)
        return wrapper
    return deco


def _fault(f):
    return {**f, "machine_name": system.machines.get(f["machine_id"], {}).get("name", f["machine_id"])}


def _me(user):
    return {"username": user.username, "full_name": user.full_name, "role": user.role, "session_min": user.session_min}


def _result(ok, message="", **extra):
    return jsonify({"ok": ok, "message": message, **extra}), (200 if ok else 400)


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


# ---- sign in (FR-26, FR-28 to FR-28d) ----
@app.post("/api/signin")
def signin():
    body = request.get_json(silent=True) or {}
    with feed.lock:
        session, message = system.accounts.sign_in(str(body.get("username", "")), str(body.get("password", "")))
        if session is None:
            return jsonify({"ok": False, "message": message}), 401
        return jsonify({"ok": True, "token": session.token, "user": _me(system.accounts.users[session.username])})


@app.post("/api/signout")
@authed()
def signout():
    with feed.lock:
        system.accounts.sign_out(_token())
    return jsonify({"ok": True})


@app.get("/api/me")
@authed()
def me():
    return jsonify(_me(g.user))


@app.post("/api/me/ping")
@authed(touch=True)
def ping():
    return jsonify({"ok": True})


@app.post("/api/me/password")
@authed(touch=True)
def change_password():
    body = request.get_json(silent=True) or {}
    with feed.lock:
        ok, message = system.accounts.change_own_password(g.user, str(body.get("old", "")), str(body.get("new", "")))
        if ok:
            save_accounts()
    return _result(ok, message)


@app.post("/api/me/session")
@authed(touch=True)
def session_minutes():
    body = request.get_json(silent=True) or {}
    with feed.lock:
        ok, message = system.accounts.set_session_minutes(_token(), body.get("minutes"))
        if ok:
            save_accounts()
    return _result(ok, message)


# ---- machines and live data ----
@app.get("/api/machines")
@authed()
def machines():
    with feed.lock:
        return jsonify([{**m, "parameters": PARAMETERS[m["type"]]} for m in system.machine_list()])


@app.get("/api/overview")
@authed()
def overview():
    return jsonify(feed.snapshot())


# ---- faults ----
@app.get("/api/faults")
@authed()
def faults():
    """For one person: the pop-ups (open, not acknowledged by them) and the bell list (open, acknowledged by them). FR-7, FR-8b."""
    with feed.lock:
        user = g.user
        shown = lambda fs: [_fault(f) for f in fs if f["machine_id"] in system.machines]   # a fault saved for a machine that is not registered now is left out
        return jsonify({"popups": shown(system.faults.popups_for(user)),
                        "bell": shown(system.faults.bell_for(user)),
                        "storage_alerts": len(system.store.admin_alerts) if user.role == "administrator" else 0})


@app.get("/api/faults/history")
@authed()
def fault_history():
    """FR-10: everyone can view fault history."""
    with feed.lock:
        return jsonify([_fault(f) for f in sorted(system.faults.history(request.args.get("machine_id")), key=lambda f: -f["raised_at"])])


@app.post("/api/faults/<int:fault_id>/acknowledge")
@authed(touch=True)
def acknowledge(fault_id):
    with feed.lock:
        ok, message = system.faults.acknowledge(fault_id, g.user)
    return _result(ok, message)


@app.post("/api/faults/<int:fault_id>/resolve")
@authed(touch=True)
def resolve(fault_id):
    with feed.lock:
        ok, message = system.faults.resolve(fault_id, g.user)
    return _result(ok, message)


@app.post("/api/machines/<machine_id>/maintenance")
@authed(touch=True)
def maintenance(machine_id):
    body = request.get_json(silent=True) or {}
    with feed.lock:
        if machine_id not in system.machines:
            return _result(False, "Unknown machine.")
        if body.get("on"):
            ok, message = system.start_maintenance(machine_id, body.get("minutes"), g.user)
            if ok:
                feed.last_window = {key: value for key, value in feed.last_window.items() if key[0] != machine_id}
        else:
            ok, message = system.end_maintenance(machine_id, g.user)
    return _result(ok, message)


@app.get("/api/machines/<machine_id>/history")
@authed()
def machine_history(machine_id):
    span = reports.RANGES.get(request.args.get("range", "day"), 86400)
    with feed.lock:
        return jsonify(reports.history(system, machine_id, request.args.get("parameter"), span))


@app.get("/api/report")
@authed("report", touch=True)
def report():
    """FR-10: Operators and Engineers make reports."""
    with feed.lock:
        text = reports.report(system, request.args.get("machine_id") or None, reports.RANGES.get(request.args.get("range", "day"), 86400))
    return Response(text, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=fault-report.csv"})


# ---- limits (FR-23, FR-23a, FR-23b) ----
@app.get("/api/limits")
@authed()
def limits():
    with feed.lock:
        machines = []
        for machine in system.machine_list():
            machines.append({**machine, "limits": {
                parameter: config.MACHINE_LIMITS.get(machine["id"], {}).get(
                    parameter, config.LIMITS[machine["type"]][parameter])
                for parameter in PARAMETERS[machine["type"]]
            }})
        return jsonify({"machines": machines, "history": system.admin.limit_history()[::-1][:50],
                        "trend_fraction": config.TREND_FRACTION, "window_s": config.WINDOW_S})


@app.post("/api/limits")
@authed("change_limits", touch=True)
def change_limit():
    body = request.get_json(silent=True) or {}
    with feed.lock:
        ok, message = system.admin.change_limit(g.user, parameter=body.get("parameter"),
                                                machine_id=body.get("machine_id"), **(body.get("limits") or {}))
    return _result(ok, message)


# ---- admin (FR-21a, FR-22, FR-27) ----
@app.get("/api/admin")
@authed("manage_users")
def admin_view():
    with feed.lock:
        st = system.store
        return jsonify({
            "users": [{"username": u.username, "full_name": u.full_name, "role": u.role} for u in system.accounts.users.values()],
            "machines": system.machine_list(),
            "storage": {"used": round(st.local.used_fraction(), 4), "cap_mb": config.LOCAL_STORAGE_CAP_MB, "alert_at": config.STORAGE_ALERT_AT,
                        "online_available": st.online.available, "online_simulated": st.online.simulated, "pending": len(st.pending_online),
                        "temp_buffer": len(st.temp_buffer), "alerts": len(st.admin_alerts), "events": st.events[-15:][::-1]},
            "change_log": system.admin.change_log[::-1][:100]})


@app.post("/api/admin/users")
@authed("manage_users", touch=True)
def admin_add_user():
    body = request.get_json(silent=True) or {}
    with feed.lock:
        user, message = system.admin.add_user(g.user, str(body.get("username", "")).strip(), str(body.get("full_name", "")).strip(),
                                               body.get("role"), str(body.get("password", "")))
        if user:
            save_accounts()
    return _result(user is not None, message)


@app.delete("/api/admin/users/<username>")
@authed("manage_users", touch=True)
def admin_remove_user(username):
    with feed.lock:
        if username == g.user.username:
            return _result(False, "You cannot remove your own account.")
        ok, message = system.admin.remove_user(g.user, username)
        if ok:
            save_accounts()
    return _result(ok, message)


@app.post("/api/admin/machines")
@authed("manage_machines", touch=True)
def admin_add_machine():
    body = request.get_json(silent=True) or {}
    machine_id = str(body.get("id", "")).strip()
    if not machine_id or " " in machine_id:
        return _result(False, "Give the machine an id without spaces.")
    with feed.lock:
        ok, message = system.admin.register_machine(g.user, machine_id, str(body.get("name") or machine_id).strip(), body.get("type"))
    return _result(ok, message)


@app.delete("/api/admin/machines/<machine_id>")
@authed("manage_machines", touch=True)
def admin_remove_machine(machine_id):
    with feed.lock:
        ok, message = system.admin.remove_machine(g.user, machine_id)
    return _result(ok, message)


# ---- demo control (Segment 5). Any signed-in person may use it, so the presenter can work from any tab. ----
@app.post("/api/demo")
@authed(touch=True)
def demo():
    body = request.get_json(silent=True) or {}
    try:
        delay = min(max(float(body.get("delay") or 0), 0.0), 120.0)
    except (TypeError, ValueError):
        delay = 0.0
    ok, message = feed.inject(body.get("action"), body.get("machine_id"), body.get("parameter"), body.get("minutes"),
                              delay=delay, schedule_id=body.get("schedule_id"))
    return _result(ok, message)


# ---- proof (Segment 5) ----
@app.get("/api/requirements")
@authed()
def requirements():
    return jsonify(proof.requirements())


@app.post("/api/checks/run")
@authed(touch=True)
def run_checks():
    return _result(proof.start_checks(), "Checks started." )


@app.get("/api/checks/status")
@authed()
def checks_status():
    return jsonify(proof.checks_status())


@app.get("/api/metrics")
@authed()
def metrics():
    with feed.lock:
        return jsonify(proof.metrics(feed, len(viewers), peak["viewers"]))


# ---- the live connection: a signed-in token is needed (FR-28) ----
@socketio.on("connect")
def on_connect(auth=None):
    with feed.lock:
        session = system.accounts.session_for((auth or {}).get("token", ""), touch=False)
    if session is None:
        return False
    viewers.add(request.sid)
    peak["viewers"] = max(peak["viewers"], len(viewers))
    emit("overview", feed.snapshot())


@socketio.on("disconnect")
def on_disconnect(*args):
    viewers.discard(request.sid)


if __name__ == "__main__":
    socketio.start_background_task(feed.run)
    options = {}
    if os.getenv("SSL_CERT") and os.getenv("SSL_KEY"):         # FR-28e: a real certificate
        options["ssl_context"] = (os.environ["SSL_CERT"], os.environ["SSL_KEY"])
    elif os.getenv("HTTPS") == "adhoc":                        # FR-28e: a self-made certificate, for the demo
        options["ssl_context"] = "adhoc"
    socketio.run(app, host="127.0.0.1", port=5000, allow_unsafe_werkzeug=True, **options)
