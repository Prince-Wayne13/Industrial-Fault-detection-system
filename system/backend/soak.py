"""Timed run for the demonstration: the real clock, the real engine, 5 minutes without stopping.
Plays a fixed list of scenarios through the live feed (the same code the Demo page uses) and measures what happened.
Run:  python soak.py 300 run1     (seconds, label)      Result goes to soak_<label>.json"""
import json
import sys
import threading
import time

import clock
import config
from live import LiveFeed
from storage import DualStore, LocalStore, OnlineStore
from system import System

SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
LABEL = sys.argv[2] if len(sys.argv) > 2 else "run"

# second -> (action, machine, parameter)
TIMELINE = {
    5: ("spike", "motor-1", "temperature"),
    20: ("warning", "motor-1", "temperature"),
    60: ("clear", "motor-1", "temperature"),
    70: ("fluctuate", "pump-1", "rpm"),
    110: ("clear", "pump-1", "rpm"),
    120: ("silent", "ups-1", "fan_rpm"),
    135: ("clear", "ups-1", "fan_rpm"),
    150: ("bad", "pump-1", "current"),
    170: ("cut_link", None, None),
    200: ("restore_link", None, None),
    220: ("critical", "motor-2", "vibration"),
    250: ("clear_all", None, None),
    270: ("heavy_load", None, None),
}

clock.use_real()
system = System(store=DualStore(LocalStore(":memory:", 512), OnlineStore(None, ":memory:")))
for who in ("operator", "engineer", "administrator"):
    system.connect(system.users[who])
closes, emits, errors = [], [0], [0]
feed = LiveFeed(system, emit_status=lambda w: closes.append(time.time()), emit_overview=lambda o: emits.__setitem__(0, emits[0] + 1))

steps, step_ms, late = 0, [], 0
started = time.time()
log = []
while steps < SECONDS:
    tick = time.time()
    sec = steps
    if sec in TIMELINE:
        a, m, p = TIMELINE[sec]
        ok, msg = feed.inject(a, m, p)
        log.append({"second": sec, "action": a, "machine": m, "parameter": p, "ok": ok, "message": msg})
    try:
        with feed.lock:
            feed.step()
    except Exception as e:           # noqa: BLE001
        errors[0] += 1
        log.append({"second": sec, "error": repr(e)})
    steps += 1
    took = time.time() - tick
    step_ms.append(took * 1000)
    if took > 1.0:
        late += 1
    time.sleep(max(0.0, 1.0 - took))
wall = time.time() - started

windows_gaps = sorted({round(b - a, 1) for a, b in zip(closes, closes[1:]) if b - a > 2})   # gaps between closes of different windows
faults = list(system.faults.faults.values())
res = {
    "label": LABEL, "planned_seconds": SECONDS, "wall_seconds": round(wall, 1), "steps": steps, "steps_over_1s": late,
    "errors": errors[0], "readings_received": system.engine.counts["received"], "invalid_readings": system.engine.counts["invalid"],
    "windows_closed": system.engine.counts["windows"], "overview_updates": emits[0],
    "step_ms_avg": round(sum(step_ms) / len(step_ms), 2), "step_ms_max": round(max(step_ms), 2),
    "window_gap_seconds": windows_gaps,
    "faults_raised": len(faults), "faults": [{"machine": f["machine_id"], "parameter": f["parameter"], "level": f["level"], "value": f.get("value"),
                                            "limit": f.get("limit"), "reason": f.get("reason"), "alert_latency_s": f["alert_latency_s"], "delayed": f["delayed"]} for f in faults],
    "max_alert_latency_s": max((f["alert_latency_s"] for f in faults), default=0),
    "alerts_delayed": system.faults.alerts_delayed,
    "stored_local": len(system.store.local.windows("motor-1")), "pending_online": len(system.store.pending_online),
    "timeline": log,
}
json.dump(res, open(f"soak_{LABEL}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("timeline", "faults")}, indent=1))
