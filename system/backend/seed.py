"""Seed data. All sensor readings, and every injection, come from here. Step 1.2.
FR-1, FR-2, FR-3, FR-24: machines and their parameters. FR-3a: one reading per second.
Nothing is random without a fixed seed, so a scenario gives the same result every time."""
import random

import clock
import config

PARAMETERS = {
    "motor": ["temperature", "current", "vibration", "rpm"],
    "pump": ["temperature", "current", "vibration", "rpm"],     # temperature = bearing temperature
    "ups": ["temperature", "current", "fan_rpm"],               # temperature = internal temperature
}

# Starting values for normal running.
NORMAL = {
    "motor": {"temperature": 90, "current": 28, "vibration": 1.8, "rpm": 1480},
    "pump": {"temperature": 65, "current": 12, "vibration": 2.0, "rpm": 1450},
    "ups": {"temperature": 50, "current": 5, "fan_rpm": 2500},
}

DEMO_MACHINES = [
    {"id": "motor-1", "name": "Motor 1", "type": "motor"},
    {"id": "motor-2", "name": "Motor 2", "type": "motor"},
    {"id": "motor-3", "name": "Motor 3", "type": "motor"},
    {"id": "pump-1", "name": "Pump 1", "type": "pump"},
    {"id": "ups-1", "name": "UPS 1", "type": "ups"},
]


# The machines the running app starts with. For now there are two motors. To bring pumps or backup power back, add them here
# (for example {"id": "pump-1", "name": "Pump 1", "type": "pump"}). DEMO_MACHINES above is the larger set the self-checks use.
LIVE_MACHINES = [
    {"id": "motor-1", "name": "Motor 1", "type": "motor"},
    {"id": "motor-2", "name": "Motor 2", "type": "motor"},
]


def make_machines(count):
    """For the heavy-load test (PR-003): 10 or more machines across the three types."""
    kinds = ["motor", "pump", "ups"]
    return [{"id": f"{kinds[i % 3]}-{i + 1}", "name": f"{kinds[i % 3].title()} {i + 1}", "type": kinds[i % 3]}
            for i in range(count)]


def normal_reading(machine, parameter, rng=random, t=None):
    base = NORMAL[machine["type"]][parameter]
    return {"machine_id": machine["id"], "parameter": parameter,
            "value": round(rng.gauss(base, base * 0.01), 2), "time": clock.now() if t is None else t}


class Source:
    """The simulated sensors. Ask it for the readings of one second.
    overrides[(machine_id, parameter)] = a number, or a function of time that returns a number (or None for 'normal').
    silent = parameters that send nothing."""

    def __init__(self, machines, seed=7, noise=1.0):
        self.machines = machines
        self.rng = random.Random(seed)
        self.noise = noise
        self.overrides = {}
        self.silent = set()

    def readings_at(self, t):
        out = []
        for m in self.machines:
            for p in PARAMETERS[m["type"]]:
                key = (m["id"], p)
                if key in self.silent:
                    continue
                target = self.overrides.get(key)
                if callable(target):
                    target = target(t)
                if target is None:
                    base = NORMAL[m["type"]][p]
                    value = round(self.rng.gauss(base, base * 0.01 * self.noise), 2)
                else:
                    value = round(self.rng.gauss(target, abs(target) * 0.005 * self.noise), 2)
                out.append({"machine_id": m["id"], "parameter": p, "value": value, "time": t})
        return out


# ---- the labelled set (Appendix D, NFR-1, NFR-2). Labels come from how each window is BUILT, not from the limits. ----

def _band(machine_type, parameter, truth, rng):
    r = config.LIMITS[machine_type][parameter]
    if truth == "critical":
        return rng.uniform(r["critical"] * 1.03, r["critical"] * 1.25)
    if truth == "warning":
        return rng.uniform(r["warning"] * 1.03, r["critical"] * 0.97)
    sides = []
    if r.get("abnormal") is not None:
        sides.append("up")
    if r.get("abnormal_below") is not None:
        sides.append("down")
    if rng.choice(sides) == "up":
        return rng.uniform(r["abnormal"] * 1.03, r["abnormal"] * 1.3)
    return rng.uniform(r["abnormal_below"] * 0.7, r["abnormal_below"] * 0.97)


def _clip_near(limit, side, rng, lo, hi, sd):
    """One reading near a limit with noise. side = 'under' keeps it on the safe side, 'over' keeps it beyond."""
    v = limit * rng.uniform(lo, hi) + rng.gauss(0, abs(limit) * sd)
    return min(v, limit * 0.998) if side == "under" else max(v, limit * 1.005)


def noisy_windows(rng, per_case=30):
    """Windows close to a limit, with noise. Labels come from how each window is BUILT (NFR-1, NFR-2).
    near_normal: every reading stays under the limit.  near_fault: every reading is over it by 1 to 6 percent.
    brief: two to four readings over, the rest under (FR-6: never a fault).  swing: pump speed that swings (SRS A.4)."""
    out = []
    for mt, params in config.LIMITS.items():
        for p, r in params.items():
            top = r.get("warning") if r.get("warning") is not None else r.get("abnormal")
            levels = [("warning", r["warning"]), ("critical", r["critical"])] if r.get("critical") is not None else \
                     ([("abnormal", r["abnormal"])] if r.get("abnormal") is not None else [])
            for _ in range(per_case):
                if top is not None:                                                 # upper limit
                    out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "near_normal",
                                "values": [_clip_near(top, "under", rng, 0.93, 0.99, 0.015) for _ in range(config.WINDOW_S)]})
                    k = rng.randrange(2, 5)
                    vals = [_clip_near(top, "under", rng, 0.93, 0.99, 0.015) for _ in range(config.WINDOW_S)]
                    for i in rng.sample(range(config.WINDOW_S), k):
                        vals[i] = top * rng.uniform(1.02, 1.10)
                    if r.get("critical") is None or True:
                        vals = [min(v, r["critical"] * 0.97) if r.get("critical") is not None else v for v in vals]
                    out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "brief", "values": vals})
                    for name, lim in levels:
                        hi = 1.06
                        if name == "warning":
                            hi = min(1.06, (r["critical"] * 0.97) / lim)
                        out.append({"machine_type": mt, "parameter": p, "truth": name, "kind": "near_fault",
                                    "values": [min(_clip_near(lim, "over", rng, 1.01, hi, 0.01), lim * hi) for _ in range(config.WINDOW_S)]})
                else:                                                               # lower limit only
                    low = r["abnormal_below"]
                    out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "near_normal",
                                "values": [max(low * rng.uniform(1.01, 1.07) + rng.gauss(0, low * 0.01), low * 1.002) for _ in range(config.WINDOW_S)]})
                    out.append({"machine_type": mt, "parameter": p, "truth": "abnormal", "kind": "near_fault",
                                "values": [min(low * rng.uniform(0.94, 0.99) + rng.gauss(0, low * 0.01), low * 0.998) for _ in range(config.WINDOW_S)]})
                if r.get("fluctuation_cv") is not None:
                    base = NORMAL[mt][p]
                    out.append({"machine_type": mt, "parameter": p, "truth": "abnormal", "kind": "swing",
                                "values": [base * (1.08 if i % 2 else 0.92) * rng.gauss(1, 0.005) for i in range(config.WINDOW_S)]})
                    out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "noisy",
                                "values": [rng.gauss(base, base * 0.03) for _ in range(config.WINDOW_S)]})
    return out


def labelled_windows(rng, per_case=30):
    """Windows of 10 values with the true answer. Includes lone spikes and half-way ramps, whose true answer is 'normal' (FR-6)."""
    out = []
    for mt, params in config.LIMITS.items():
        for p in params:
            r = config.LIMITS[mt][p]
            levels = ["warning", "critical"] if r.get("critical") is not None else ["abnormal"]
            base = NORMAL[mt][p]
            for _ in range(per_case):
                out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "normal",
                            "values": [rng.gauss(base, base * 0.01) for _ in range(config.WINDOW_S)]})
                spike = [rng.gauss(base, base * 0.01) for _ in range(config.WINDOW_S)]
                spike[rng.randrange(config.WINDOW_S)] = _band(mt, p, levels[-1], rng)
                out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "spike", "values": spike})
                for lv in levels:                                  # partway windows: f of the 10 readings over the limit, the rest normal. FR-6
                    f = rng.randrange(1, 10)
                    level = _band(mt, p, lv, rng)
                    vals = [rng.gauss(level, abs(level) * 0.01) for _ in range(f)] + [rng.gauss(base, base * 0.01) for _ in range(config.WINDOW_S - f)]
                    rng.shuffle(vals) if rng.random() < 0.5 else None      # sometimes a ramp, sometimes scattered
                    truth = lv if f / config.WINDOW_S >= config.TREND_FRACTION else "normal"
                    out.append({"machine_type": mt, "parameter": p, "truth": truth, "kind": "ramp", "values": vals})
                for lv in levels:
                    out.append({"machine_type": mt, "parameter": p, "truth": lv, "kind": "fault",
                                "values": [_band(mt, p, lv, rng) for _ in range(config.WINDOW_S)]})
    out += noisy_windows(rng, per_case)
    rng.shuffle(out)
    return out
