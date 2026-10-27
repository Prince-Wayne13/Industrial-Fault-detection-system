"""The check script. Step 1.8. One command, one table: python check_all.py
Plays every seeded scenario through the real engine and prints PASS or FAIL for each requirement the back end can prove.
Requirements that need a screen are listed with the segment that shows them. A copy of the table goes to check_report.md."""
import pathlib
import sys
import traceback

import clock
import config
import demo
import metrics
import model
from seed import PARAMETERS, make_machines

CHECKS = []
LATER = {   # needs a screen or a later feature: requirement -> (segment, what)
    "FR-10": (3, "history and report on the machine page"), "FR-11": (5, "Bluetooth / Wi-Fi mode on the demo panel"),
    "FR-28e": (5, "HTTPS certificate"), "NFR-5": (5, "uptime measured over the demo"), "NFR-8": (2, "all machines on one screen"),
    "PR-002": (2, "reading to screen within 2 seconds"), "PR-004": (5, "5 viewers at once"), "PR-007": (5, "start-up within 60 seconds"),
}


def check(req, title):
    def deco(fn):
        CHECKS.append((req, title, fn))
        return fn
    return deco


def fresh(name=None, connect=("operator", "engineer", "administrator"), **kw):
    s = demo.new_system(**kw)
    for u in connect:
        s.connect(s.users[u])
    return s, (demo.play(s, name) if name else {})


def need(cond, msg):
    if not cond:
        raise AssertionError(msg)


def faults_of(s):
    return list(s.faults.faults.values())


# ---------------- detection ----------------
@check("FR-1", "Motor shows temperature, current, vibration, RPM")
def _():
    s, _f = fresh("Normal running")
    need(set(s.dashboard("motor-1")) == {"temperature", "current", "vibration", "rpm"}, s.dashboard("motor-1"))
    return "4 parameters on every motor"

@check("FR-2", "Pump shows bearing temperature, current, vibration, RPM")
def _():
    s, _f = fresh("Normal running")
    need(set(s.dashboard("pump-1")) == set(PARAMETERS["pump"]), s.dashboard("pump-1"))
    return "4 parameters"

@check("FR-3", "UPS shows internal temperature, current, fan speed")
def _():
    s, _f = fresh("Normal running")
    need(set(s.dashboard("ups-1")) == {"temperature", "current", "fan_rpm"}, s.dashboard("ups-1"))
    return "3 parameters"

@check("FR-3a", "One reading per second per parameter")
def _():
    s, _f = fresh("Normal running")
    need(s.engine.counts["received"] == 19 * 61, s.engine.counts)
    kept = sum(w["n"] for w in s.store.local.windows("motor-1") if w["parameter"] == "temperature")
    need(kept == 60, kept)
    return "61 seconds gave 61 readings per parameter (60 stored, 1 in the open window)"

@check("FR-4", "A sustained high reading is flagged")
def _():
    s, _f = fresh("Sustained warning")
    need(s.latest_status[("motor-1", "temperature")]["status"] == "warning", s.latest_status[("motor-1", "temperature")]["status"])
    return "Motor 1 temperature flagged"

@check("FR-5", "Warning, critical, and abnormal where only one level exists")
def _():
    s, _f = fresh("Sustained warning")
    need(faults_of(s)[0]["level"] == "warning", "warning expected")
    s2, _f = fresh("Sustained critical")
    f = faults_of(s2)[0]
    need(f["level"] == "critical" and f["machine_id"] == "motor-1" and f["parameter"] == "temperature", f)
    s3 = demo.new_system()
    demo._sustained(s3, {("pump-1", "temperature"): 200})            # far above 95, still only 'abnormal'
    need(faults_of(s3)[0]["level"] == "abnormal", faults_of(s3))
    need(model.levels_for("pump", "temperature") == ("normal", "abnormal"), "levels")
    need(model.levels_for("motor", "vibration") == ("normal", "warning", "critical"), "levels")
    return "motor temperature/current/vibration have 3 statuses; pump temperature, rpm, UPS and others have 2"

@check("FR-6", "One abnormal reading is never a fault")
def _():
    s, _f = fresh("Lone spike")
    need(faults_of(s) == [], faults_of(s))
    need(all(w["status"] == "normal" for w in s.store.local.windows("motor-1") if w["parameter"] == "temperature"), "status")
    s2, _f = fresh("Sustained warning")
    need(faults_of(s2)[0]["raised_at"] >= demo.T0 + 20, "fault appeared before the window ended")
    s3 = demo.new_system()                                           # SRS A.4: pump speed that swings is abnormal, one low reading is not
    base = 1450
    s3.connect(s3.users["operator"])
    src = demo.Source(s3.machine_list())
    t0 = clock.now()
    src.overrides[("pump-1", "rpm")] = lambda t: base * (1.08 if int(t) % 2 else 0.92) if t >= t0 + 5 else None
    demo.run(s3, 31, src)
    rpm = [f for f in faults_of(s3) if f["parameter"] == "rpm"]
    need(len(rpm) == 1 and rpm[0]["level"] == "abnormal" and rpm[0]["reason"] == "fluctuating", faults_of(s3))
    s4 = demo.new_system()
    src4 = demo.Source(s4.machine_list())
    src4.overrides[("pump-1", "rpm")] = lambda t: 900 if int(t) == int(t0) + 8 else None
    demo.run(s4, 31, src4)
    need([f for f in faults_of(s4) if f["parameter"] == "rpm"] == [], "one low speed reading became a fault")
    return "spike: no fault. Sustained: fault only when the 10-second window ended. Pump speed swing: abnormal; one low reading: none"

# ---------------- alerts ----------------
@check("FR-7", "Pop-up for every connected Operator and Engineer")
def _():
    s, _f = fresh("Sustained warning")
    need(len(s.popups_for(s.users["operator"])) == 1 and len(s.popups_for(s.users["engineer"])) == 1, "popups")
    return "both see it (screen in Segment 3)"

@check("FR-7a", "Pop-up carries machine, parameter, type, level, time")
def _():
    s, _f = fresh("Sustained warning")
    f = s.popups_for(s.users["operator"])[0]
    need(all(k in f for k in ("machine_id", "parameter", "level", "raised_at", "limit", "value")), f)
    need(f["value"] > f["limit"], f)                                   # the pop-up can say "140 now, limit 130"
    return "all fields present, including the reading and the limit (screen in Segment 3)"

@check("FR-7b", "Administrator gets no fault alerts")
def _():
    s, _f = fresh("Sustained warning")
    adm = s.users["administrator"]
    need(s.popups_for(adm) == [] and s.faults.bell_for(adm) == [], "admin got an alert")
    return "no pop-up, no bell list"

@check("FR-7c", "Nobody connected: fault stays open and is shown to the next person")
def _():
    s, f = fresh("Nobody connected", connect=())
    need(f["open_faults"] == 1 and s.popups_for(s.users["operator"]) == [], "should wait")
    s.connect(s.users["operator"])
    need(len(s.popups_for(s.users["operator"])) == 1, "not shown on connect")
    return "shown when the Operator connects"

@check("FR-8", "Each person acknowledges for themselves")
def _():
    s, _f = fresh("Sustained warning")
    op, eng = s.users["operator"], s.users["engineer"]
    fid = faults_of(s)[0]["id"]
    need(s.faults.acknowledge(fid, op)[0], "ack failed")
    need(s.popups_for(op) == [] and len(s.popups_for(eng)) == 1, "Engineer's pop-up must stay")
    need(not s.faults.acknowledge(fid, s.users["administrator"])[0], "Administrator must not acknowledge")
    return "Operator's pop-up goes, Engineer's stays"

@check("FR-8a", "Acknowledging records who and when")
def _():
    s, _f = fresh("Sustained warning")
    fid = faults_of(s)[0]["id"]
    s.faults.acknowledge(fid, s.users["operator"])
    a = s.faults.faults[fid]["acknowledged_by"][0]
    need(a["user"] == "operator1" and a["time"] > 0, a)
    return str(a["user"])

@check("FR-8b", "Acknowledging does not close the fault")
def _():
    s, _f = fresh("Sustained warning")
    fid = faults_of(s)[0]["id"]
    s.faults.acknowledge(fid, s.users["operator"])
    need(s.faults.faults[fid]["status"] == "open", "closed")
    need(len(s.faults.bell_for(s.users["operator"])) == 1, "bell list")
    return "still open; shows in the bell list"

# ---------------- data ----------------
@check("FR-9", "Faults and readings can be called up")
def _():
    s, _f = fresh("Sustained warning")
    need(len(s.faults.history("motor-1")) == 1, "history")
    w = s.store.local.windows("motor-1", status="warning")
    need(w and len(w[0]["readings"]) == 10, w)
    return "fault history and the 10 readings of the warning window"

@check("FR-9a", "Every 10-second window keeps its status and time")
def _():
    s, _f = fresh("Normal running")
    w = [x for x in s.store.local.windows("motor-1") if x["parameter"] == "temperature"]
    need(len(w) == 6 and all(x["status"] == "normal" for x in w), len(w))
    need(all(round(b["start_time"] - a["start_time"]) == 10 for a, b in zip(w, w[1:])), "spacing")
    return "6 windows in 60 seconds, 10 seconds apart"

@check("FR-9b", "Normal readings go after 24 hours; warning and critical stay")
def _():
    s, f = fresh("Old data")
    w = s.store.local.windows("motor-1")
    old_normal = [x for x in w if x["status"] == "normal" and x["start_time"] < clock.now() - 3600 * 24]
    need(f["cleaned"] == 5 and all(x["readings"] == [] for x in old_normal), "old normal readings remain")
    need(all(len(x["readings"]) == 10 for x in w if x["status"] in ("warning", "critical")), "fault readings lost")
    need(any(x["status"] == "normal" and len(x["readings"]) == 10 for x in w), "recent normal readings lost")
    need(len(w) == 8, "statuses were deleted")
    return "5 old normal windows cleared, statuses all kept, warning/critical readings kept"

@check("FR-12", "Connection cut: keep collecting, send on restore")
def _():
    s, f = fresh("Connection cut")
    need(f["pending_during_cut"] > 0 and f["sent_on_restore"] == f["pending_during_cut"], f)
    need(s.store.local.count_windows() > 0 and s.latest_status, "local data stopped")
    need(s.store.online.count_readings() == s.store.local.count_readings(), "stores differ after restore")
    return f"{f['sent_on_restore']} windows held locally and sent on restore"

@check("FR-13", "Silent sensor flagged within 3 seconds")
def _():
    s, f = fresh("Sensor goes silent")
    t = s.sensor_faults[("motor-2", "rpm")]
    need(t - (f["silent_from"] - 1) <= config.SENSOR_TIMEOUT_S, t)
    d = s.dashboard("motor-2")["rpm"]
    need(d["sensor_fault"] and d["value"] is None, d)
    return "dashboard shows a sensor fault, not the last number"

@check("FR-14", "Wrong type, missing and impossible readings are rejected and logged")
def _():
    s, f = fresh("Bad reading")
    reasons = {x["reason"] for x in s.engine.invalid_log}
    need(reasons == {"wrong type", "missing", "impossible value"}, reasons)
    need(faults_of(s) == [] and s.engine.counts["windows"] > 0, "system did not carry on")
    need(s.dashboard("motor-1")["temperature"]["value"] is not None, "dashboard")
    return "3 rejected, logged, system carried on"

@check("NFR-7", "Noisy data: no corrupt reading acted on")
def _():
    s, _f = fresh("Noisy readings")
    need(faults_of(s) == [] and s.engine.counts["invalid"] == 0, (len(faults_of(s)), s.engine.counts))
    s2, _f = fresh("Bad reading")
    need(all(w["n"] == 10 for w in s2.store.local.windows("motor-1")), "bad readings reached a window")
    return "noise at 3x raises no fault; bad readings never enter a window"

@check("FR-15", "One fault record per abnormal parameter")
def _():
    s, _f = fresh("Two faults at once")
    need({(f["machine_id"], f["parameter"]) for f in faults_of(s)} == {("motor-1", "temperature"), ("motor-1", "current")}, faults_of(s))
    return "2 records"

@check("FR-16", "No second alert while a fault is open")
def _():
    s, f = fresh("Fault returns")
    need((f["after_first"], f["after_repeat_while_open"], f["after_resolve_and_return"]) == (1, 1, 2), f)
    return "1 record while open, a new one only after it was resolved and came back"

@check("FR-17", "Only an Engineer resolves, after acknowledging; time recorded")
def _():
    s, _f = fresh("Sustained warning")
    fid, op, eng = faults_of(s)[0]["id"], s.users["operator"], s.users["engineer"]
    need(not s.faults.resolve(fid, op)[0], "operator resolved")
    need(not s.faults.resolve(fid, eng)[0], "resolved without acknowledging")
    s.faults.acknowledge(fid, eng)
    need(s.faults.resolve(fid, eng)[0] and s.faults.faults[fid]["resolved_at"], "resolve failed")
    need(s.faults.bell_for(eng) == [], "bell count did not drop")
    return "Operator refused, Engineer needs to acknowledge first, bell count drops"

@check("FR-18", "Maintenance mode: readings and alerts paused")
def _():
    s, _f = fresh("Maintenance")
    need(faults_of(s) == [] and not s.faults.suppressed, "new alert was raised or suppressed")
    need(not s.store.local.windows("motor-1") and ("motor-1", "temperature") not in s.latest_reading, "maintenance readings were recorded")
    need("motor-1" in s.engine.paused_machines, "sensor feed was not paused")
    return "no readings or alerts while the machine is in maintenance"

@check("FR-19", "Overdue maintenance is flagged")
def _():
    s, _f = fresh("Maintenance")
    need(s.faults.overdue("motor-1") and not s.faults.overdue("motor-2"), "overdue flag")
    return "Motor 1 overdue after its stated minute"

@check("FR-20", "Storage full: keep readings, no crash, event logged")
def _():
    s, f = fresh("Storage fails", local_cap_mb=0.25)
    need(f["temp"] > 0 and any(e["kind"] == "local_store_full" for e in s.store.events), s.store.events[:2])
    return f"{f['temp']} windows in temporary storage"

@check("FR-21", "Restart: last settings and open faults come back")
def _():
    s, f = fresh("Restart")
    new = f["system"]
    need(config.MACHINE_LIMITS["motor-1"]["temperature"]["warning"] == 135, "machine limit lost")
    need(len([x for x in new.faults.faults.values() if x["status"] == "open"]) == 1, "open fault lost")
    need(new.latest_status and new.engine.counts["windows"] > 0, "no status after new readings")
    return "limit 135 kept, fault kept, status back after fresh readings"

@check("FR-21a", "Storage alert at 75% goes to the Administrator only")
def _():
    s, f = fresh("Storage fills up", local_cap_mb=0.25)
    need(len(s.store.admin_alerts) == 1 and s.store.admin_alerts[0]["to"] == "administrator", s.store.admin_alerts)
    need(0.75 <= f["used_at_alert"] < 1.0, f)
    need(all(s.popups_for(s.users[u]) == [] for u in ("operator", "engineer")), "users got the alert")
    return f"alert at {f['used_at_alert']:.0%}"

@check("NFR-10", "Nothing deleted automatically before 75%")
def _():
    s, _f = fresh("Storage fills up", local_cap_mb=0.25)
    need(s.store.local.count_windows() == s.engine.counts["windows"], "windows were deleted")
    return "every window saved so far is still there"

# ---------------- admin and limits ----------------
@check("FR-22", "Change log: who and when")
def _():
    s, _f = fresh("Limit change")
    e = s.admin.change_log[-1]
    need(e["who"] == "engineer1" and e["when"] > 0, e)
    return "engineer1 changed the limit"

@check("FR-23", "Old value and date kept when a limit changes")
def _():
    s, _f = fresh("Limit change")
    e = s.admin.limit_history(parameter="temperature", machine_id="motor-1")[-1]
    need(e["old"]["warning"] == 130 and e["new"]["warning"] == 135 and e["when"] > 0, e)
    return "130 kept next to 135"

@check("FR-23a", "Engineer changes a limit, no restart")
def _():
    s, f = fresh("Limit change")
    need(f["ok"][0] and not f["op_refused"][0], f)
    need(config.MACHINE_LIMITS["motor-1"]["temperature"]["warning"] == 135, "machine limit not updated")
    need(model.rule_for("motor", "temperature", "motor-2")["warning"] == 130, "another motor inherited the change")
    return "works; Operator refused (screen in Segment 4)"

@check("FR-23b", "Warning limit must stay below critical")
def _():
    s, f = fresh("Limit change")
    need(not f["bad_refused"][0] and "below" in f["bad_refused"][1], f["bad_refused"])
    return f["bad_refused"][1]

@check("FR-23c", "A new limit applies to later readings only")
def _():
    s, f = fresh("Limit change")
    need(f["last_status_after"] == "normal" and f["old_windows_unchanged"], f)
    return "132 was a warning at 130, normal at 135; old windows unchanged"

@check("FR-23d", "Each fault stores the limit in force when it was raised")
def _():
    s, _f = fresh("Limit change")
    need(faults_of(s)[0]["limit"] == 130, faults_of(s)[0])
    return "fault shows 130 although the limit is now 135"

@check("FR-24", "Several machines of one type are separate units")
def _():
    s, _f = fresh("Sustained warning")
    need(s.latest_status[("motor-2", "temperature")]["status"] == "normal" and not s.faults.history("motor-2"), "motor-2")
    need(len(s.faults.history("motor-1")) == 1, "motor-1")
    return "Motor 1 faulted; Motors 2 and 3 untouched"

@check("FR-25", "One time source")
def _():
    here = pathlib.Path(__file__).parent
    bad = [p.name for p in here.glob("*.py") if p.name not in ("clock.py", "check_all.py") and "time.time(" in p.read_text()]
    need(not bad, bad)
    s, _f = fresh("Sustained warning")
    f = faults_of(s)[0]
    need(f["raised_at"] >= f["confirmed_at"], f)
    return "only clock.py reads the computer clock"

@check("FR-26", "Sign-out time 1 to 5 minutes, own setting")
def _():
    s, f = fresh("Login checks")
    need(f["set1"] and f["set5"] and not f["set6"] and f["expired"], f)
    need(config.SESSION_DEFAULT_MIN == 5, "default")
    return "1 and 5 accepted, 6 refused, idle session expired"

@check("FR-27", "Administrator-only functions")
def _():
    s, f = fresh("Login checks")
    need("Only the Administrator" in f["op_creates_user"], f)
    need(not s.admin.register_machine(s.users["engineer"], "m9", "Motor 9", "motor")[0], "engineer registered a machine")
    need(s.admin.register_machine(s.users["administrator"], "motor-9", "Motor 9", "motor")[0], "admin refused")
    need(not hasattr(s.accounts, "reset_password"), "password reset exists")
    return "Operator/Engineer refused; Administrator allowed; no password reset exists"

@check("FR-28", "Sign in first")
def _():
    s, f = fresh("Login checks")
    need(f["no_session"] is None and f["session"] is not None, f)
    return "no session -> sign-in page"

@check("FR-28a", "Passwords: 14 refused, 15 and 64 accepted")
def _():
    s, f = fresh("Login checks")
    need("at least 15" in f["len14"] and f["len15"] and f["len64"], f)
    return "ok"

@check("FR-28b", "No forced mix of characters")
def _():
    s, f = fresh("Login checks")
    need(f["plain_ok"], f)
    return "all-lowercase accepted"

@check("FR-28c", "Common passwords refused")
def _():
    s, f = fresh("Login checks")
    need("too common" in f["common"], f["common"])
    return f["common"]

@check("FR-28d", "5 wrong passwords block the account for 15 minutes")
def _():
    s, f = fresh("Login checks")
    need("blocked for 15 minutes" in f["wrong_pw"][-1] and "blocked" in f["blocked_msg"] and f["after_block"], f)
    return f["wrong_pw"][-1]

@check("FR-28f", "Passwords stored salted and scrambled")
def _():
    s, f = fresh("Login checks")
    from auth import hash_password
    need(f["hash_is_not_password"] and s.accounts.users["operator1"].pw_hash.startswith(b"$2"), "hash")
    need(hash_password("same-long-password-1") != hash_password("same-long-password-1"), "no salt")
    return "bcrypt, different every time"

# ---------------- measured ----------------
@check("NFR-1", "At least 95% of critical temperature and current faults found")
def _():
    r = model.evaluate()["critical_temp_current"]
    need(r[0] / r[1] >= 0.95, r)
    return f"{r[0]} of {r[1]} = {r[0] / r[1]:.0%}"

@check("NFR-2", "At least 85% of vibration faults found")
def _():
    r = model.evaluate()["vibration"]
    need(r[0] / r[1] >= 0.85, r)
    return f"{r[0]} of {r[1]} = {r[0] / r[1]:.0%}"

@check("NFR-6", "At least 99% of readings stored, also during a cut")
def _():
    s, _f = fresh("Connection cut")
    s.flush()
    made = s.engine.counts["received"] - s.engine.counts["invalid"]
    local, online = s.store.local.count_readings(), s.store.online.count_readings()
    need(local / made >= 0.99 and online / made >= 0.99, (made, local, online))
    return f"generated {made}, local {local}, online {online}"

@check("NFR-9", "One parameter's logic changes on its own")
def _():
    import copy
    s = demo.new_system()
    before = copy.deepcopy(config.LIMITS)
    s.admin.change_limit(s.users["engineer"], "motor", "vibration", warning=3.0)
    changed = [(m, p) for m in before for p in before[m] if before[m][p] != config.LIMITS[m][p]]
    need(changed == [("motor", "vibration")], changed)
    return "only motor vibration changed"

@check("PR-001", "Status updates at least every 10 seconds")
def _():
    s, _f = fresh("Normal running")
    w = [x for x in s.store.local.windows("pump-1") if x["parameter"] == "rpm"]
    need(all(round(b["start_time"] - a["start_time"]) <= 10 for a, b in zip(w, w[1:])), "gap")
    return "every 10 seconds"

@check("PR-001a", "Critical alert within 2 seconds of the status")
def _():
    s, _f = fresh("Sustained critical")
    f = faults_of(s)[0]
    need(f["alert_latency_s"] <= config.ALERT_LIMIT_S and not f["delayed"], f)
    return f"{f['alert_latency_s']} s"

@check("PR-001b", "A late alert is still shown, logged and flagged")
def _():
    s, _f = fresh("Slow alert")
    f = faults_of(s)[0]
    need(f["delayed"] and s.faults.alerts_delayed and s.faults.delayed_log and len(s.popups_for(s.users["operator"])) == 1, f)
    return f"alert came after {f['alert_latency_s']} s: shown, logged, 'alerts delayed' set"

@check("PR-003", "10 machines at the same time")
def _():
    s, f = fresh("Heavy load", machines=make_machines(10))
    need(len(s.machines) == 10 and s.engine.counts["windows"] > 0 and faults_of(s) == [], f)
    w = [x for x in s.store.local.windows("motor-1") if x["parameter"] == "temperature"]
    need(all(round(b["start_time"] - a["start_time"]) == 10 for a, b in zip(w, w[1:])), "status gaps")
    return "10 machines, status every 10 s (screen timing in Segment 5)"

@check("PR-005", "At least 40 readings per second")
def _():
    s, f = fresh("Heavy load", machines=make_machines(10))
    need(f["per_second"] >= 40, f)
    return f"{f['per_second']:,.0f} readings per second processed"

@check("PR-006", "Room for 3,456,000 readings plus statuses and faults")
def _():
    mb = metrics.projected_mb()
    need(mb <= config.LOCAL_STORAGE_CAP_MB, mb)
    return f"about {mb} MB needed for one day; the local file is set to {config.LOCAL_STORAGE_CAP_MB:g} MB"


def main():
    rows = []
    for req, title, fn in CHECKS:
        try:
            detail, ok = fn(), True
        except AssertionError as e:
            detail, ok = f"{e}", False
        except Exception:
            detail, ok = traceback.format_exc().splitlines()[-1], False
        rows.append((req, title, "PASS" if ok else "FAIL", str(detail)))
    for req, (seg, what) in LATER.items():
        rows.append((req, what, f"SEGMENT {seg}", ""))
    order = lambda r: (r[0].split("-")[0] != "FR", r[0].split("-")[0] != "NFR", r[0].split("-")[0], int("".join(c for c in r[0].split("-")[1] if c.isdigit())), r[0])
    rows.sort(key=order)
    width = max(len(r[1]) for r in rows)
    lines = [f"{r[0]:<8}{r[2]:<11}{r[1]:<{width + 2}}{r[3]}" for r in rows]
    print("\n".join(lines))
    passed = sum(r[2] == "PASS" for r in rows)
    failed = sum(r[2] == "FAIL" for r in rows)
    later = len(rows) - passed - failed
    summary = f"\n{passed} PASS, {failed} FAIL, {later} to be shown in later segments"
    print(summary)
    md = ["# Check report: Segment 1", "", "| Requirement | Result | What was checked | Detail |", "| --- | --- | --- | --- |"]
    md += [f"| {r[0]} | {r[2]} | {r[1]} | {r[3]} |" for r in rows]
    md += ["", summary.strip(), ""]
    pathlib.Path(__file__).with_name("check_report.md").write_text("\n".join(md), encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
