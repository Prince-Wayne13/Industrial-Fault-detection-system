"""Fault records and their life. Open -> acknowledged (each person for themselves) -> resolved. Step 1.4.

FR-7, FR-7a, FR-7b, FR-7c   pop-up to every connected Operator and Engineer; never to the Administrator
FR-8, FR-8a, FR-8b          each person acknowledges for themselves; record who and when; acknowledging does not close it
FR-15                       one fault record per abnormal parameter
FR-16                       no duplicate alert while a fault is open
FR-17                       only an Engineer resolves, after acknowledging; record when
FR-18, FR-19                maintenance mode for a stated time; alerts pause; overdue flag
FR-23d                      each fault stores the limit in force when it was raised
PR-001a, PR-001b            alert within 2 seconds of the status confirming it; a late alert is shown, logged and flagged

A "pop-up" is any open fault the person has not acknowledged yet (popups_for). So a fault raised while nobody is
connected is shown to the next Operator or Engineer who connects (FR-7c), and the Administrator never gets one (FR-7b).
The "bell list" is the open faults the person has acknowledged (bell_for)."""
import clock
from auth import can
from config import ALERT_LIMIT_S, RANK


class FaultStore:
    def __init__(self, persist=None):
        self.persist = persist or (lambda fault: None)
        self.faults = {}
        self.next_id = 1
        self.maintenance = {}       # machine_id -> {"by", "started", "until", "minutes"}
        self.suppressed = []        # alerts held back during maintenance (FR-18)
        self.delayed_log = []       # PR-001b
        self.alerts_delayed = False # the dashboard's "Alerts delayed" notice

    def load(self, records):
        """After a restart: bring the saved faults back (FR-21)."""
        self.faults = {f["id"]: f for f in records}
        self.next_id = max(self.faults, default=0) + 1

    # ---- raising ----
    def open_for(self, machine_id, parameter):
        for f in self.faults.values():
            if f["status"] == "open" and f["machine_id"] == machine_id and f["parameter"] == parameter:
                return f
        return None

    def raise_fault(self, machine_id, parameter, level, limit, confirmed_at):
        """Returns (fault, why). `why` is 'new', 'already open' or 'maintenance'."""
        now = clock.now()
        if self.in_maintenance(machine_id):
            self.suppressed.append({"machine_id": machine_id, "parameter": parameter, "level": level, "time": now})
            return None, "maintenance"
        existing = self.open_for(machine_id, parameter)
        if existing:                                   # FR-16: no second pop-up. A worse level is noted on the same record.
            if RANK[level] > RANK[existing["level"]]:
                existing["escalations"].append({"level": level, "limit": limit, "time": now})
                existing["level"] = level
                self.persist(existing)
            return existing, "already open"
        latency = now - confirmed_at
        fault = {"id": self.next_id, "machine_id": machine_id, "parameter": parameter, "level": level,
                 "limit": limit,                                  # FR-23d: the limit in force when it was raised
                 "status": "open", "confirmed_at": confirmed_at, "raised_at": now,
                 "alert_latency_s": round(latency, 3), "delayed": latency > ALERT_LIMIT_S,
                 "acknowledged_by": [], "resolved_by": None, "resolved_at": None, "escalations": [], "last_normal_at": None}
        self.next_id += 1
        self.faults[fault["id"]] = fault
        if fault["delayed"]:                                      # PR-001b
            self.alerts_delayed = True
            self.delayed_log.append({"fault_id": fault["id"], "latency_s": fault["alert_latency_s"], "time": now})
        self.persist(fault)
        return fault, "new"

    def note_normal(self, machine_id, parameter, t):
        f = self.open_for(machine_id, parameter)
        if f:
            f["last_normal_at"] = t          # the reading came back to normal; the fault stays open until resolved

    # ---- who sees what ----
    def popups_for(self, user):
        if user.role not in ("operator", "engineer"):
            return []                                           # FR-7b
        return [f for f in self.faults.values()
                if f["status"] == "open" and user.username not in [a["user"] for a in f["acknowledged_by"]]]

    def bell_for(self, user):
        if user.role not in ("operator", "engineer"):
            return []
        return [f for f in self.faults.values()
                if f["status"] == "open" and user.username in [a["user"] for a in f["acknowledged_by"]]]

    # ---- acknowledging and resolving ----
    def acknowledge(self, fault_id, user):
        if not can(user.role, "acknowledge"):
            return False, "Only an Operator or an Engineer can acknowledge a fault."
        f = self.faults.get(fault_id)
        if f is None:
            return False, "No such fault."
        if f["status"] != "open":
            return False, "That fault is already resolved."
        if user.username in [a["user"] for a in f["acknowledged_by"]]:
            return True, ""
        f["acknowledged_by"].append({"user": user.username, "role": user.role, "time": clock.now()})   # FR-8a
        self.persist(f)
        return True, ""                                         # FR-8b: the fault stays open

    def resolve(self, fault_id, engineer):
        if not can(engineer.role, "resolve"):
            return False, "Only an Engineer can mark a fault resolved."
        f = self.faults.get(fault_id)
        if f is None or f["status"] != "open":
            return False, "No open fault with that number."
        if engineer.username not in [a["user"] for a in f["acknowledged_by"]]:
            return False, "Acknowledge the fault before resolving it."
        f["status"] = "resolved"
        f["resolved_by"] = engineer.username
        f["resolved_at"] = clock.now()                          # FR-17
        self.persist(f)
        return True, ""

    def history(self, machine_id=None):
        """FR-9, FR-10: everyone can call up the fault history."""
        return [f for f in self.faults.values() if machine_id in (None, f["machine_id"])]

    # ---- maintenance ----
    def set_maintenance(self, machine_id, minutes, engineer):
        if not can(engineer.role, "maintenance"):
            return False, "Only an Engineer can use maintenance mode."
        if not isinstance(minutes, (int, float)) or minutes <= 0:
            return False, "Give the time in minutes."
        now = clock.now()
        self.maintenance[machine_id] = {"by": engineer.username, "started": now, "minutes": minutes, "until": now + minutes * 60}
        return True, ""

    def end_maintenance(self, machine_id, engineer):
        if not can(engineer.role, "maintenance"):
            return False, "Only an Engineer can use maintenance mode."
        return (self.maintenance.pop(machine_id, None) is not None), ""

    def in_maintenance(self, machine_id):
        return machine_id in self.maintenance

    def overdue(self, machine_id):
        """FR-19: still in maintenance after the stated time."""
        m = self.maintenance.get(machine_id)
        return bool(m) and clock.now() >= m["until"]
