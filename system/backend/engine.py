"""The engine. A reading splits into two streams the moment it arrives. See docs/design/engine.md. Step 1.3.

  Stream 1: straight to the dashboard (every reading, even a wrong one).
  Stream 2: checker -> status model (10-second window) -> status -> save to both stores.

Time comes from the reading's own time stamp, which comes from clock.py (FR-25)."""
import clock
from checker import check_reading
from config import WINDOW_S, SENSOR_TIMEOUT_S
from model import classify
from seed import PARAMETERS


class Engine:
    def __init__(self, machines, send_live=None, send_status=None, save_window=None, on_sensor_fault=None, on_sensor_back=None):
        self.machines = machines                       # machine_id -> machine type. Shared with the System, so registering a machine reaches here.
        self.send_live = send_live or (lambda r: None)
        self.send_status = send_status or (lambda w: None)
        self.save_window = save_window or (lambda w: None)
        self.on_sensor_fault = on_sensor_fault or (lambda key, t: None)
        self.on_sensor_back = on_sensor_back or (lambda key, t: None)
        self.buffer = {}          # (machine_id, parameter) -> [(time, value)] clean readings of this window
        self.last_seen = {}       # (machine_id, parameter) -> time of last reading (FR-13)
        self.silent = set()
        self.paused_machines = set()
        self.connection_paused = False
        self.invalid_log = []     # FR-14
        self.window_started = None
        self.counts = {"received": 0, "invalid": 0, "windows": 0}

    def handle_reading(self, reading):
        self.counts["received"] += 1
        t = reading.get("time", clock.now()) if isinstance(reading, dict) else clock.now()
        key = (reading.get("machine_id"), reading.get("parameter")) if isinstance(reading, dict) else (None, None)
        if self.connection_paused or key[0] in self.paused_machines:
            return
        self.last_seen[key] = t
        if key in self.silent:
            self.silent.discard(key)
            self.on_sensor_back(key, t)
        ok, reason = check_reading(reading)
        if ok:
            mtype = self.machines.get(key[0])
            if mtype is None:
                ok, reason = False, "unknown machine"
            elif key[1] not in PARAMETERS[mtype]:
                ok, reason = False, "unknown parameter"
        self.send_live({**(reading if isinstance(reading, dict) else {}), "valid": ok, "reason": reason})   # stream 1
        if not ok:
            self.counts["invalid"] += 1
            self.invalid_log.append({"reading": reading, "reason": reason, "time": t})      # kept out of the model, logged (FR-14)
            return
        if self.window_started is None:
            self.window_started = t
        if t - self.window_started >= WINDOW_S:
            self.close_window(t)
        self.buffer.setdefault(key, []).append((t, reading["value"]))                       # stream 2

    def check_silence(self, now):
        """Call every second. A parameter with no reading for SENSOR_TIMEOUT_S seconds is flagged once. FR-13."""
        fresh = []
        for key, seen in self.last_seen.items():
            if not self.connection_paused and key[0] not in self.paused_machines and key not in self.silent and now - seen >= SENSOR_TIMEOUT_S:
                self.silent.add(key)
                fresh.append(key)
                self.on_sensor_fault(key, now)
        return fresh

    def pause_machine(self, machine_id):
        self.paused_machines.add(machine_id)
        self.buffer = {key: items for key, items in self.buffer.items() if key[0] != machine_id}
        if not self.buffer:
            self.window_started = None
        for key in [key for key in self.last_seen if key[0] == machine_id]:
            self.last_seen.pop(key, None)
            self.silent.discard(key)
            self.on_sensor_back(key, clock.now())

    def resume_machine(self, machine_id):
        self.paused_machines.discard(machine_id)

    def pause_connection(self):
        self.connection_paused = True
        self.buffer.clear()
        self.window_started = None
        for key in list(self.last_seen):
            self.last_seen.pop(key, None)
            self.silent.discard(key)
            self.on_sensor_back(key, clock.now())

    def resume_connection(self):
        self.connection_paused = False

    def close_window(self, t):
        """Set the status of every parameter for the window that just ended, then save it. FR-5, FR-6, FR-9a."""
        closed = []
        for key, items in self.buffer.items():
            if not items:
                continue
            values = [v for _, v in items]
            window = {"machine_id": key[0], "parameter": key[1], "machine_type": self.machines[key[0]],
                      "start_time": self.window_started, "end_time": items[-1][0],
                      "status": classify(self.machines[key[0]], key[1], values, key[0]),
                      "readings": values, "n": len(values), "confirmed_at": clock.now()}
            self.send_status(window)
            self.save_window(window)
            closed.append(window)
        self.counts["windows"] += len(closed)
        self.buffer = {}
        self.window_started = t
        return closed

    def flush(self):
        """Close the window that is still open (end of a run or a planned stop)."""
        return self.close_window(clock.now()) if self.buffer else []
