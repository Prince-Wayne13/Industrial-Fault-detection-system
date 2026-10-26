"""Seed data. All sensor readings, and every injection, come from here. Step 2.
FR-1, FR-2, FR-3, FR-24: machines and their parameters. FR-3a: one reading per second."""
import random
import time

PARAMETERS = {
    "motor": ["temperature", "current", "vibration", "rpm"],
    "pump": ["temperature", "current", "vibration", "rpm"],     # temperature = bearing temperature
    "ups": ["temperature", "current", "fan_rpm"],               # temperature = internal temperature
}

# Starting values for normal running. Adjust them when the screens exist.
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


def normal_reading(machine, parameter):
    base = NORMAL[machine["type"]][parameter]
    return {"machine_id": machine["id"], "parameter": parameter,
            "value": round(random.gauss(base, base * 0.01), 2), "time": time.time()}
