"""The demo control panel. Step 9. FR-11 near and remote mode, FR-12 cut and restore the connection, DC-006.
Each scenario is seed data played in order. The list matches docs/design/test-plan.md."""

SCENARIOS = [
    "Normal running", "Lone spike", "Sustained warning", "Sustained critical", "Two faults at once",
    "Sensor goes silent", "Bad reading", "Connection cut", "Storage fills up", "Storage fails", "Restart",
    "Maintenance", "Fault returns", "Limit change", "Nobody connected", "Noisy readings", "Heavy load",
    "Slow alert", "Labelled test set", "Login checks", "Near and remote mode", "Old data",
]


def play(name):
    raise NotImplementedError("step 9")
