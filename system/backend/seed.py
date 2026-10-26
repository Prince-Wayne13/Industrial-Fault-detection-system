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
                k = rng.randrange(3, 8)
                ramp = [rng.gauss(base, base * 0.01) for _ in range(k)] + \
                       [_band(mt, p, levels[0], rng) for _ in range(config.WINDOW_S - k)]
                out.append({"machine_type": mt, "parameter": p, "truth": "normal", "kind": "ramp", "values": ramp})
                for lv in levels:
                    out.append({"machine_type": mt, "parameter": p, "truth": lv, "kind": "fault",
                                "values": [_band(mt, p, lv, rng) for _ in range(config.WINDOW_S)]})
    rng.shuffle(out)
    return out
