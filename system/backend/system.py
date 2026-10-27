"""The whole back end wired together. Step 1.3 to 1.6. The Flask app (Segment 2) and the check script both use this class."""
import copy

import clock
import config
from admin import Admin
from auth import Accounts
from engine import Engine
from faults import FaultStore
from model import fluctuation, is_fluctuating, limit_in_force, observed_value, rule_for, threshold_level
from seed import DEMO_MACHINES
from storage import DualStore, LocalStore, OnlineStore

DEMO_USERS = {      # key: (username, full name, role). Passwords are long on purpose (FR-28a).
    "administrator": ("admin1", "Alice Administrator", "administrator"),
    "engineer": ("engineer1", "Eric Engineer", "engineer"),
    "engineer2": ("engineer2", "Esther Engineer", "engineer"),
    "operator": ("operator1", "Oscar Operator", "operator"),
    "operator2": ("operator2", "Olivia Operator", "operator"),
}


def demo_password(username):
    return f"demo-password-for-{username}"


class System:
    def __init__(self, machines=None, store=None, accounts=None, local_cap_mb=None, alert_hold=0.0, restarted=False):
        if store is None:
            store = DualStore(LocalStore(":memory:", local_cap_mb), OnlineStore(None, ":memory:"))
        self.store = store
        if restarted:                                    # FR-21: resume with the last known settings
            saved = store.local.get_setting("limits")
            if saved:
                config.LIMITS.clear()
                config.LIMITS.update(saved)
            config.MACHINE_LIMITS.clear()
            config.MACHINE_LIMITS.update(store.local.get_setting("machine_limits", {}))
            if config.USE_SAVED_MACHINES:
                machines = store.local.get_setting("machines", machines)
        else:
            config.reset_limits()
        self.machines = {m["id"]: dict(m) for m in (machines or copy.deepcopy(DEMO_MACHINES))}
        self.machine_types = {}                          # id -> type, kept in step with self.machines by sync_types()
        self.alert_hold = alert_hold                     # the demo's "slow alert" injection (I-11)
        self.latest_status = {}                          # (machine_id, parameter) -> last window
        self.latest_reading = {}                         # (machine_id, parameter) -> last reading, with valid flag
        self.sensor_faults = {}                          # (machine_id, parameter) -> time flagged
        self.connected = {}                              # username -> user
        self.accounts = accounts or Accounts()
        self.users = {}
        if accounts is None:
            for key, (uname, full, role) in DEMO_USERS.items():
                self.accounts._add(uname, full, role, demo_password(uname))
        for key, (uname, _, _) in DEMO_USERS.items():
            if uname in self.accounts.users:
                self.users[key] = self.accounts.users[uname]
        self.faults = FaultStore(persist=self.store.save_fault)
        if restarted:
            self.faults.load(store.local.faults())
        self.admin = Admin(self.accounts, self.machines, store, saved_log=store.local.logs() if restarted else None)
        self.faults.log = self.admin.record
        self.engine = Engine(self.machine_types, send_live=self._live, send_status=self._status, save_window=self.store.save_window,
                             on_sensor_fault=lambda k, t: self.sensor_faults.__setitem__(k, t),
                             on_sensor_back=lambda k, t: self.sensor_faults.pop(k, None))
        self.sync_types()

    def sync_types(self):
        self.machine_types.clear()
        self.machine_types.update({i: m["type"] for i, m in self.machines.items()})

    def machine_list(self):
        return list(self.machines.values())

    # ---- data in ----
    def ingest(self, reading):
        self.sync_types()
        if self.engine.connection_paused or (isinstance(reading, dict) and reading.get("machine_id") in self.engine.paused_machines):
            return
        self.engine.handle_reading(reading)

    def start_maintenance(self, machine_id, minutes, engineer):
        ok, message = self.faults.set_maintenance(machine_id, minutes, engineer)
        if ok:
            self.engine.pause_machine(machine_id)
            for key in [key for key in self.latest_status if key[0] == machine_id]:
                self.latest_status.pop(key, None)
        return ok, message

    def end_maintenance(self, machine_id, engineer):
        ok, message = self.faults.end_maintenance(machine_id, engineer)
        if ok:
            self.engine.resume_machine(machine_id)
        return ok, message

    def tick(self):
        """Call once a second."""
        self.engine.check_silence(clock.now())

    def flush(self):
        self.engine.flush()

    def _live(self, reading):
        self.latest_reading[(reading.get("machine_id"), reading.get("parameter"))] = reading

    def _status(self, window):
        key = (window["machine_id"], window["parameter"])
        self.latest_status[key] = window
        if window["status"] == "normal":
            self.faults.note_normal(key[0], key[1], window["end_time"])
            return
        if self.alert_hold:
            clock.advance(self.alert_hold)               # injection: hold the alert back
        mt, par, vals = window["machine_type"], key[1], window["readings"]
        value = max(vals) if vals else None
        limit = limit_in_force(mt, par, window["status"], value, key[0])
        shown, reason = observed_value(mt, par, vals, key[0]), None
        if vals and is_fluctuating(mt, par, vals, key[0]) and all(threshold_level(mt, par, v, key[0]) == "normal" for v in vals):
            limit, reason = rule_for(mt, par, key[0])["fluctuation_step"], "fluctuating"      # a spread fault: no reading crossed a limit
            shown = round(fluctuation(mt, par, vals), 4)
        self.faults.raise_fault(key[0], key[1], window["status"], limit, window["confirmed_at"], value=shown, reason=reason)

    # ---- what the dashboard reads ----
    def dashboard(self, machine_id):
        """Per parameter: the live value, its marks, and the last status. FR-13: a silent sensor shows a fault, not the last number."""
        out = {}
        for (mid, p), r in self.latest_reading.items():
            if mid != machine_id:
                continue
            silent = (mid, p) in self.sensor_faults
            out[p] = {"value": None if silent else r.get("value"), "invalid": not r.get("valid", True) and not silent,
                      "sensor_fault": silent, "status": self.latest_status.get((mid, p), {}).get("status", "unknown")}
        return out

    # ---- people ----
    def connect(self, user):
        self.connected[user.username] = user

    def disconnect(self, user):
        self.connected.pop(user.username, None)

    def popups_for(self, user):
        return self.faults.popups_for(user) if user.username in self.connected else []

    def restart(self):
        """A planned stop and start. Settings and faults come back from the local store. FR-21."""
        return System(store=self.store, accounts=self.accounts, alert_hold=self.alert_hold, restarted=True)
