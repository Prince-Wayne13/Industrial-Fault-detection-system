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
