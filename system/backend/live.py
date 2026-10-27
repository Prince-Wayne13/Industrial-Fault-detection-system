"""The live feed for the dashboard. Segment 2. FR-3a one reading per second, FR-13, FR-14, FR-18, FR-19, PR-001b, PR-002.

Plays the simulated sensors in real time through the real engine (System.ingest). Two things go out to the screens:
  stream 1  every reading, the moment it arrives (emit_reading)
  stream 2  every status, the moment a 10-second window closes (emit_status); the engine saves it to both stores
plus one full snapshot per second (emit_overview) that carries the marks: Sensor fault, Invalid, Maintenance, Overdue, Alerts delayed.

inject() is the demo control (the Demo page calls it). It changes what the simulated sensors send; nothing else."""
import threading
import time
import traceback

import clock
import config
from config import RANK
from model import threshold_level
from seed import PARAMETERS, Source

BAD_VALUE = 99999      # outside every physical range, so the checker rejects it (FR-14)
BAD_SECONDS = 5        # how long a demo bad reading lasts
PARAM_ACTIONS = {"warning", "critical", "spike", "clear", "bad", "silent"}
NO_MACHINE = {"slow_alert_on", "slow_alert_off", "cut_link", "restore_link", "heavy_load", "remove_load"}
IMMEDIATE = {"clear_all", "cancel", "mode_near", "mode_remote"}      # never delayed
LABELS = {"warning": "Warning value", "critical": "Critical value", "spike": "One spike", "bad": "Bad reading", "silent": "Sensor goes silent",
          "clear": "Back to normal", "maintenance": "Start maintenance", "end_maintenance": "End maintenance", "slow_alert_on": "Slow alerts on",
          "slow_alert_off": "Slow alerts off", "cut_link": "Connection cut", "restore_link": "Connection restored",
          "heavy_load": "Heavy load", "remove_load": "Remove the extra machines"}
UNKNOWN = {"value": None, "invalid": False, "sensor_fault": False, "status": "unknown"}


def fault_value(machine_type, parameter, level):
    """A value that sits in the given level for this parameter, taken from the limits in force."""
    r = config.LIMITS[machine_type][parameter]
    if r.get("critical") is not None:
        return round(r["critical"] * 1.07, 2) if level == "critical" else round((r["warning"] + r["critical"]) / 2, 2)
    if r.get("abnormal") is not None:
        return round(r["abnormal"] * 1.1, 2)
    if r.get("abnormal_below") is not None:
        return round(r["abnormal_below"] * 0.8, 2)
    return None


class LiveFeed:
    def __init__(self, system, emit_reading=None, emit_status=None, emit_overview=None):
        self.system = system
        self.lock = threading.RLock()
        self.source = Source(system.machine_list())
        self.bad = {}                    # (machine_id, parameter) -> time the bad readings stop
        self.running = False
        self.scheduled = []              # demo actions waiting for their start time: shown as a countdown on every screen
        self.last_window = {}            # (machine_id, parameter) -> the last closed window: values, level of each reading, status
        self._next_id = 1
        self.mode = "near"               # FR-11: simulated near-range (Bluetooth) or remote-range (Wi-Fi) mode
        self.started = clock.real()
        self.ready_at = None             # PR-007: set when the first second of data has gone out
        self.latency = {"n": 0, "sum": 0.0, "max": 0.0}   # PR-002: a reading's time inside the server, in milliseconds
        self._arrived = clock.real()
        self._cleaned = clock.real()      # FR-9b: the 24-hour clean-up runs once an hour
        self.emit_reading = emit_reading or (lambda r: None)
        self.emit_status = emit_status or (lambda w: None)
        self.emit_overview = emit_overview or (lambda o: None)
        engine = system.engine
        send_live, send_status = engine.send_live, engine.send_status

        def live(reading):
            send_live(reading)
            level = None
            mtype = engine.machines.get(reading.get("machine_id"))
            if reading.get("valid") and mtype and isinstance(reading.get("value"), (int, float)):
                level = threshold_level(mtype, reading["parameter"], reading["value"])
            self._safe(self.emit_reading, {**reading, "level": level})   # stream 1, straight to the dashboard, with the level of this one reading
            ms = (clock.real() - self._arrived) * 1000
            self.latency["n"] += 1
            self.latency["sum"] += ms
            self.latency["max"] = max(self.latency["max"], ms)

        def status(window):
            levels = [threshold_level(window["machine_type"], window["parameter"], v) for v in window["readings"]]
            summary = {"values": window["readings"], "levels": levels, "status": window["status"], "start": window["start_time"]}
            self.last_window[(window["machine_id"], window["parameter"])] = summary
            self._safe(self.emit_status, {**{k: window[k] for k in ("machine_id", "parameter", "status", "end_time")}, **summary})
            send_status(window)                                          # stream 2: status goes out first, then faults are raised

        engine.send_live, engine.send_status = live, status

    @staticmethod
    def _safe(fn, arg):
        try:
            fn(arg)
        except Exception:                # a screen that cannot be reached must never stop the engine (NFR-7)
            traceback.print_exc()

    # ---- the loop ----
    def step(self):
        t = clock.now()
        due = [i for i in self.scheduled if i["at"] <= t]
        self.scheduled = [i for i in self.scheduled if i["at"] > t]
        for i in due:
            self._apply(i["action"], i["machine_id"], i["parameter"], i["minutes"], in_step=True)
        self.source.machines = self.system.machine_list()
        for r in self.source.readings_at(t):
            if self.bad.get((r["machine_id"], r["parameter"]), 0) > t:
                r["value"] = BAD_VALUE
            self._arrived = clock.real()
            self.system.ingest(r)
        self.bad = {k: until for k, until in self.bad.items() if until > t}
        self.system.engine.check_silence(t)
        self._safe(self.emit_overview, self.snapshot())
        if self.ready_at is None:
            self.ready_at = clock.real()
        if clock.real() - self._cleaned > 3600:
            self._cleaned = clock.real()
            self.system.store.cleanup()

    def run(self):
        self.running = True
        while self.running:
            started = clock.real()
            try:
                with self.lock:
                    self.step()
            except Exception:
                traceback.print_exc()
            time.sleep(max(0.0, 1.0 - (clock.real() - started)))

    def stop(self):
        self.running = False

    # ---- what the dashboard reads ----
    def snapshot(self):
        with self.lock:
            s = self.system
            machines = []
            for m in s.machine_list():
                dash = s.dashboard(m["id"])
                params = {}
                for p in PARAMETERS[m["type"]]:
                    buf = s.engine.buffer.get((m["id"], p), [])
                    params[p] = {**(dash.get(p) or UNKNOWN),
                                 "window": {"start": s.engine.window_started, "length": config.WINDOW_S,
                                            "readings": [[round(t, 3), v, threshold_level(m["type"], p, v)] for t, v in buf]},
                                 "last": self.last_window.get((m["id"], p))}
                worst = max((v["status"] for v in params.values()), key=lambda x: RANK.get(x, -1))
                machines.append({**m, "status": worst, "maintenance": s.faults.in_maintenance(m["id"]),
                                 "overdue": s.faults.overdue(m["id"]), "parameters": params})
            return {"machines": machines, "alerts_delayed": s.faults.alerts_delayed, "time": clock.now(), "mode": self.mode,
                    "link": "up" if s.store.online.available else "cut", "pending": len(s.store.pending_online),
                    "scheduled": [{"id": i["id"], "label": i["label"], "at": i["at"]} for i in self.scheduled]}

    def _person(self, role):
        return next((u for u in self.system.accounts.users.values() if u.role == role), None)

    # ---- demo control ----
    def inject(self, action, machine_id=None, parameter=None, minutes=None, delay=0, schedule_id=None):
        """Start a demo action now, or after `delay` seconds. A delayed action shows as a countdown on every screen."""
        with self.lock:
            s = self.system
            if action == "cancel":
                before = len(self.scheduled)
                self.scheduled = [i for i in self.scheduled if i["id"] != schedule_id]
                return len(self.scheduled) < before, "Cancelled." if len(self.scheduled) < before else "Nothing to cancel."
            if delay and delay > 0 and action not in IMMEDIATE:
                machine = s.machines.get(machine_id)
                if action not in NO_MACHINE and machine is None:
                    return False, "Choose a machine."
                if action in PARAM_ACTIONS and parameter not in PARAMETERS[machine["type"]]:
                    return False, "Choose a parameter."
                label = LABELS.get(action, action) + (f" · {machine['name']}" if machine and action not in NO_MACHINE else "") \
                    + (f" {parameter}" if action in PARAM_ACTIONS else "")
                self.scheduled.append({"id": self._next_id, "action": action, "machine_id": machine_id, "parameter": parameter,
                                       "minutes": minutes, "at": clock.now() + delay, "label": label})
                self._next_id += 1
                return True, f"{label} starts in {int(delay)} seconds."
            return self._apply(action, machine_id, parameter, minutes)

    def _apply(self, action, machine_id=None, parameter=None, minutes=None, in_step=False):
        with self.lock:
            s = self.system
            if action == "clear_all":
                self.scheduled.clear()
                self.source.overrides.clear()
                self.source.silent.clear()
                self.bad.clear()
                s.alert_hold = 0.0
                engineer = self._person("engineer")
                for mid in list(s.faults.maintenance):
                    s.faults.end_maintenance(mid, engineer)
                if not s.store.online.available:
                    s.store.restore_online()
                return True, "Everything back to normal running."
            if action in ("mode_near", "mode_remote"):
                self.mode = "near" if action == "mode_near" else "remote"
                return True, "Near range (Bluetooth) mode." if self.mode == "near" else "Remote range (Wi-Fi) mode."
            if action == "cut_link":
                s.store.online.set_available(False)               # FR-12: collecting and showing carry on; saving to the online database waits
                return True, "Connection to the online database cut. Data is kept here."
            if action == "restore_link":
                sent = s.store.restore_online()
                return True, f"Connection restored. {sent} saved windows sent."
            if action == "heavy_load":                            # PR-003: 10 or more machines at once
                admin = self._person("administrator")
                if admin is None:
                    return False, "No Administrator account to register machines."
                kinds = ["motor", "pump", "ups"]
                for i in range(1, 7):
                    mid = f"load-{i}"
                    if mid not in s.machines:
                        s.admin.register_machine(admin, mid, f"{kinds[i % 3].title()} L{i}", kinds[i % 3])
                return True, f"{len(s.machines)} machines registered."
            if action == "remove_load":
                admin = self._person("administrator")
                for mid in [m for m in s.machines if m.startswith("load-")]:
                    s.admin.remove_machine(admin, mid)
                return True, f"{len(s.machines)} machines registered."
            if action in ("slow_alert_on", "slow_alert_off"):
                s.alert_hold = 3.0 if action == "slow_alert_on" else 0.0
                return True, "Alerts will come late." if s.alert_hold else "Alerts are on time again."
            machine = s.machines.get(machine_id)
            if machine is None:
                return False, "Choose a machine."
            if action == "maintenance":
                ok, msg = s.faults.set_maintenance(machine_id, minutes if minutes else 30, self._person("engineer"))
                return ok, msg or f"{machine['name']} is in maintenance mode."
            if action == "end_maintenance":
                s.faults.end_maintenance(machine_id, self._person("engineer"))
                return True, f"{machine['name']} is out of maintenance mode."
            if parameter not in PARAMETERS[machine["type"]]:
                return False, "Choose a parameter."
            key = (machine_id, parameter)
            if action in ("warning", "critical"):
                self.source.silent.discard(key)
                self.source.overrides[key] = fault_value(machine["type"], parameter, action)
                return True, f"{machine['name']} {parameter} now reads a {action} value."
            if action == "spike":                                 # one wrong-high second: must never become a fault (FR-6)
                t0 = int(clock.now()) + (0 if in_step else 1)
                value = fault_value(machine["type"], parameter, "critical")
                self.source.overrides[key] = lambda t, t0=t0, v=value: v if int(t) == t0 else None
                return True, f"{machine['name']} {parameter} has one spike."
            if action == "clear":
                self.source.overrides.pop(key, None)
                self.source.silent.discard(key)
                self.bad.pop(key, None)
                return True, f"{machine['name']} {parameter} is back to normal."
            if action == "bad":
                self.bad[key] = clock.now() + BAD_SECONDS
                return True, f"{machine['name']} {parameter} sends a wrong reading for {BAD_SECONDS} seconds."
            if action == "silent":
                self.source.silent.add(key)
                return True, f"{machine['name']} {parameter} sends nothing."
            return False, "Unknown action."
