"""The scenario player. Step 1.2. FR-11 near and remote mode and FR-12 cut and restore the connection, DC-006.
Each scenario is seed data played in order through the real engine. The list matches docs/design/test-plan.md.

play(system, name) plays one scenario on a System and returns a dict of facts. The checks in check_all.py read the System afterwards."""
import time

import clock
import config
import model
from seed import Source, make_machines, labelled_windows
from system import System

SCENARIOS = [
    "Normal running", "Lone spike", "Sustained warning", "Sustained critical", "Two faults at once",
    "Sensor goes silent", "Bad reading", "Connection cut", "Storage fills up", "Storage fails", "Restart",
    "Maintenance", "Fault returns", "Limit change", "Nobody connected", "Noisy readings", "Heavy load",
    "Slow alert", "Labelled test set", "Login checks", "Near and remote mode", "Old data",
]

T0 = 1_800_000_000.0        # the simulated start time of every scenario


def new_system(**kw):
    clock.set_time(T0)
    return System(**kw)


def run(system, seconds, source, start=None):
    """Play `seconds` seconds of readings, one second at a time, through the engine."""
    t0 = clock.now() if start is None else start
    for s in range(seconds):
        t = t0 + s
        clock.set_time(t)
        for r in source.readings_at(t):
            system.ingest(r)
        system.tick()
    clock.set_time(t0 + seconds)
    return t0 + seconds


def _from(t_start, value):
    """An override: `value` from t_start on, normal before."""
    return lambda t: value if t >= t_start else None


def _sustained(system, overrides, seconds=31, noise=1.0):
    src = Source(system.machine_list(), noise=noise)
    t0 = clock.now()
    for key, value in overrides.items():
        src.overrides[key] = _from(t0 + 5, value)
    run(system, seconds, src)
    return src


def normal_running(system):
    run(system, 61, Source(system.machine_list()))
    return {"seconds": 61}


def lone_spike(system):
    src = Source(system.machine_list())
    t0 = clock.now()
    src.overrides[("motor-1", "temperature")] = lambda t: 200 if t == t0 + 12 else None
    run(system, 31, src)
    return {}


def sustained_warning(system):
    _sustained(system, {("motor-1", "temperature"): 140})
    return {}


def sustained_critical(system):
    _sustained(system, {("motor-1", "temperature"): 160})
    return {}


def two_faults(system):
    _sustained(system, {("motor-1", "temperature"): 140, ("motor-1", "current"): 33})
    return {}


def sensor_silent(system):
    src = Source(system.machine_list())
    t0 = clock.now()
    run(system, 10, src)
    src.silent.add(("motor-2", "rpm"))
    run(system, 10, src)
    return {"silent_from": t0 + 10}


def bad_reading(system):
    src = Source(system.machine_list())
    t0 = clock.now()
    run(system, 5, src)
    for value in ("hot", None, 99999):                 # wrong type, missing, impossible
        clock.set_time(clock.now() + 0.1)
        system.ingest({"machine_id": "motor-1", "parameter": "temperature", "value": value, "time": clock.now()})
    run(system, 26, src, start=t0 + 5)
    return {"injected": 3}


def connection_cut(system):
    src = Source(system.machine_list())
    run(system, 11, src)
    system.store.online.set_available(False)
    run(system, 20, src)
    facts = {"pending_during_cut": len(system.store.pending_online)}
    facts["sent_on_restore"] = system.store.restore_online()
    return facts


def storage_fills_up(system):
    src = Source(system.machine_list())
    for _ in range(400):                               # 10 simulated seconds at a time, until the 75% alert
        run(system, 10, src)
        if system.store.admin_alerts:
            break
    return {"used_at_alert": system.store.admin_alerts[0]["used"] if system.store.admin_alerts else None}


def storage_fails(system):
    src = Source(system.machine_list())
    for _ in range(800):
        run(system, 10, src)
        if system.store.temp_buffer:
            break
    run(system, 30, src)                               # the system keeps running after the store is full
    return {"temp": len(system.store.temp_buffer)}


def restart(system):
    _sustained(system, {("motor-1", "temperature"): 140})
    system.admin.change_limit(system.users["engineer"], "motor", "temperature", warning=135)
    new = system.restart()
    src = Source(new.machine_list())
    run(new, 21, src)
    return {"system": new}


def maintenance(system):
    eng = system.users["engineer"]
    system.faults.set_maintenance("motor-1", 1, eng)
    _sustained(system, {("motor-1", "temperature"): 140})
    clock.advance(120)                                 # fast-forward past the stated minute
    return {}


def fault_returns(system):
    eng = system.users["engineer"]
    _sustained(system, {("motor-1", "temperature"): 140})
    first = len(system.faults.faults)
    run(system, 21, Source(system.machine_list()))      # back to normal, fault still open
    _sustained(system, {("motor-1", "temperature"): 140})
    again = len(system.faults.faults)
    fid = next(iter(system.faults.faults))
    system.faults.acknowledge(fid, eng)
    system.faults.resolve(fid, eng)                    # cleared
    _sustained(system, {("motor-1", "temperature"): 140})
    return {"after_first": first, "after_repeat_while_open": again, "after_resolve_and_return": len(system.faults.faults)}


def limit_change(system):
    eng, op = system.users["engineer"], system.users["operator"]
    facts = {}
    facts["op_refused"] = system.admin.change_limit(op, "motor", "temperature", warning=135)
    facts["bad_refused"] = system.admin.change_limit(eng, "motor", "temperature", warning=160)
    _sustained(system, {("motor-1", "temperature"): 132})         # still normal at 130, warning at 135? it is above 130 -> warning
    facts["before_change_faults"] = len(system.faults.faults)
    facts["ok"] = system.admin.change_limit(eng, "motor", "temperature", warning=135)
    before = len(system.store.local.windows("motor-1", status="warning"))
    _sustained(system, {("motor-1", "temperature"): 132})         # 132 is under the new limit of 135
    facts["last_status_after"] = system.latest_status[("motor-1", "temperature")]["status"]
    facts["old_windows_unchanged"] = len(system.store.local.windows("motor-1", status="warning")) == before
    return facts


def nobody_connected(system):
    _sustained(system, {("motor-1", "temperature"): 140})
    return {"open_faults": len(system.faults.faults)}


def noisy_readings(system):
    run(system, 61, Source(system.machine_list(), noise=3.0))
    return {}


def heavy_load(system):
    src = Source(system.machine_list())
    start = time.perf_counter()
    run(system, 60, src)
    wall = time.perf_counter() - start
    n = system.engine.counts["received"]
    return {"readings": n, "wall_s": wall, "per_second": n / wall}


def slow_alert(system):
    system.alert_hold = 3.0
    _sustained(system, {("motor-1", "temperature"): 160})
    return {}


def labelled_test_set(system):
    return model.evaluate()


def login_checks(system):
    acc, admin = system.accounts, system.users["administrator"]
    facts = {}
    sess, _ = acc.sign_in("operator1", "demo-password-for-operator1")
    facts["session"] = sess
    facts["no_session"] = acc.session_for(None)
    facts["wrong_pw"] = [acc.sign_in("operator2", "not-the-right-password")[1] for _ in range(5)]
    facts["blocked_msg"] = acc.sign_in("operator2", "demo-password-for-operator2")[1]
    clock.advance(16 * 60)
    facts["after_block"] = acc.sign_in("operator2", "demo-password-for-operator2")[0] is not None
    facts["len14"] = acc.create_user(admin, "u14", "U Fourteen", "operator", "a" * 14)[1]
    facts["len15"] = acc.create_user(admin, "u15", "U Fifteen", "operator", "a" * 15)[0] is not None
    facts["len64"] = acc.create_user(admin, "u64", "U Sixtyfour", "operator", "x" * 64)[0] is not None
    facts["plain_ok"] = acc.create_user(admin, "u16", "U Plain", "operator", "alllowercaseletters")[0] is not None
    facts["common"] = acc.create_user(admin, "uc", "U Common", "operator", "password1234567")[1]
    facts["op_creates_user"] = acc.create_user(system.users["operator"], "x", "X", "operator", "long-enough-password-1")[1]
    facts["hash_is_not_password"] = b"demo-password" not in acc.users["operator1"].pw_hash
    sess2, _ = acc.sign_in("engineer1", "demo-password-for-engineer1")
    facts["set1"], facts["set5"], facts["set6"] = (acc.set_session_minutes(sess2.token, m)[0] for m in (1, 5, 6))
    acc.set_session_minutes(sess2.token, 1)
    clock.advance(61)
    facts["expired"] = acc.session_for(sess2.token) is None
    return facts


def near_and_remote(system):
    return {"skipped": "Segment 5: FR-11 is made true on the demo panel"}


def old_data(system):
    store = system.store
    old = clock.now() - 25 * 3600
    for i in range(5):
        store.save_window({"machine_id": "motor-1", "parameter": "temperature", "start_time": old + i * 10, "status": "normal",
                           "readings": [90.0] * 10, "n": 10})
    for i, status in enumerate(("warning", "critical")):
        store.save_window({"machine_id": "motor-1", "parameter": "temperature", "start_time": old + 100 + i * 10, "status": status,
                           "readings": [140.0] * 10, "n": 10})
    store.save_window({"machine_id": "motor-1", "parameter": "temperature", "start_time": clock.now(), "status": "normal",
                       "readings": [90.0] * 10, "n": 10})          # recent normal window: readings stay
    return {"cleaned": store.cleanup()}


_PLAYERS = {
    "Normal running": normal_running, "Lone spike": lone_spike, "Sustained warning": sustained_warning,
    "Sustained critical": sustained_critical, "Two faults at once": two_faults, "Sensor goes silent": sensor_silent,
    "Bad reading": bad_reading, "Connection cut": connection_cut, "Storage fills up": storage_fills_up,
    "Storage fails": storage_fails, "Restart": restart, "Maintenance": maintenance, "Fault returns": fault_returns,
    "Limit change": limit_change, "Nobody connected": nobody_connected, "Noisy readings": noisy_readings,
    "Heavy load": heavy_load, "Slow alert": slow_alert, "Labelled test set": labelled_test_set,
    "Login checks": login_checks, "Near and remote mode": near_and_remote, "Old data": old_data,
}


def play(system, name):
    return _PLAYERS[name](system)
