"""Administrator and limits. Step 1.6.
FR-22 change log (who and when), FR-23 keep the old limit and date, FR-23a Engineer changes limits without a restart,
FR-23b reject a warning limit that is not below the critical limit, FR-23c a new limit applies to later readings,
FR-27 only the Administrator manages users and machines. The Administrator cannot reset passwords."""
import config
import clock
from auth import can
from seed import PARAMETERS


class Admin:
    def __init__(self, accounts, machines, store):
        self.accounts = accounts
        self.machines = machines          # machine_id -> {"id","name","type"}. Shared with the System.
        self.store = store
        self.change_log = []              # FR-22

    def _log(self, who, what, old, new):
        entry = {"who": who, "when": clock.now(), "what": what, "old": old, "new": new}
        self.change_log.append(entry)
        return entry

    # ---- limits: Engineer (FR-23a, the one exception to FR-27) ----
    def change_limit(self, by, machine_type=None, parameter=None, machine_id=None, **new):
        """Change one machine's rule; callers without machine_id retain the type-default maintenance API."""
        if by is None or not can(by.role, "change_limits"):
            return False, "Only an Engineer can change limits."
        machine = self.machines.get(machine_id) if machine_id else None
        if machine_id and machine is None:
            return False, "Unknown machine."
        if machine:
            machine_type = machine["type"]
        base_rule = config.LIMITS.get(machine_type, {}).get(parameter)
        if machine_id:
            rule = config.MACHINE_LIMITS.get(machine_id, {}).get(parameter, base_rule)
        else:
            rule = base_rule
        if rule is None:
            return False, "Unknown machine type or parameter."
        if not new or any(k not in rule for k in new):
            return False, "That parameter has no such limit. Its limits are: " + ", ".join(rule) + "."
        for k, v in new.items():
            if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v:
                return False, "A limit must be a number."
        proposed = {**rule, **new}
        if proposed.get("warning") is not None and proposed.get("critical") is not None and proposed["warning"] >= proposed["critical"]:
            return False, "The warning limit must be below the critical limit."          # FR-23b
        old = dict(rule)
        updated = {**rule, **new}
        if machine_id:
            config.MACHINE_LIMITS.setdefault(machine_id, {})[parameter] = updated
            self.store.local.put_setting("machine_limits", config.MACHINE_LIMITS)
            what = f"limit {machine_id} {parameter}"
        else:
            rule.update(new)
            self.store.local.put_setting("limits", config.LIMITS)
            what = f"limit {machine_type} {parameter}"
        self._log(by.username, what, old, updated)                                        # FR-22, FR-23: old value and date kept
        return True, ""

    def limit_history(self, machine_type=None, parameter=None, machine_id=None):
        return [e for e in self.change_log
                if e["what"].startswith("limit") and (machine_id is None or e["what"].startswith(f"limit {machine_id} "))
                and (machine_type is None or f" {machine_type} " in e["what"] + " ")
                and (parameter is None or e["what"].endswith(parameter))]

    # ---- users and machines: Administrator only (FR-27, UC-5) ----
    def add_user(self, by, username, full_name, role, password):
        user, msg = self.accounts.create_user(by, username, full_name, role, password)
        if user:
            self._log(by.username, f"add user {username}", None, {"role": role})
        return user, msg

    def remove_user(self, by, username):
        ok, msg = self.accounts.remove_user(by, username)
        if ok:
            self._log(by.username, f"remove user {username}", None, None)
        return ok, msg

    def register_machine(self, by, machine_id, name, machine_type):
        if by is None or not can(by.role, "manage_machines"):
            return False, "Only the Administrator registers machines."
        if machine_type not in PARAMETERS:
            return False, "Unknown machine type."
        if machine_id in self.machines:
            return False, "That machine is already registered."
        self.machines[machine_id] = {"id": machine_id, "name": name, "type": machine_type}
        self.store.local.put_setting("machine_limits", config.MACHINE_LIMITS)
        self.store.local.put_setting("machines", list(self.machines.values()))
        self._log(by.username, f"register machine {machine_id}", None, machine_type)
        return True, ""

    def remove_machine(self, by, machine_id):
        if by is None or not can(by.role, "manage_machines"):
            return False, "Only the Administrator removes machines."
        if self.machines.pop(machine_id, None) is None:
            return False, "No such machine."
        config.MACHINE_LIMITS.pop(machine_id, None)
        self.store.local.put_setting("machine_limits", config.MACHINE_LIMITS)
        self.store.local.put_setting("machines", list(self.machines.values()))
        self._log(by.username, f"remove machine {machine_id}", None, None)
        return True, ""
