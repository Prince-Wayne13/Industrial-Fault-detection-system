"""Numbers for the 'measure' tests. Step 1.7 / 1.8 and Segment 5.
NFR-5 uptime, PR-001 status update time, PR-001a alert time, PR-002 dashboard time,
PR-003 10 machines, PR-004 5 users, PR-005 40 readings per second, PR-006 room for readings, PR-007 start-up within 60 seconds."""
import random

import clock
import config
from storage import LocalStore, PAGE

STARTED = clock.now()


def uptime_seconds():
    return clock.now() - STARTED


def projected_mb(readings=3_456_000, per_window=config.WINDOW_S):
    """PR-006: how big the local file gets for one day at the minimum load (10 machines x 4 parameters x 86,400 s),
    worked out from the real size of a sample of windows, plus 10% for statuses and fault records."""
    sample = 2000
    store = LocalStore(":memory:", cap_mb=512)
    rng = random.Random(3)
    for i in range(sample):
        store.save_window({"machine_id": f"motor-{i % 10}", "parameter": "temperature", "start_time": 1_800_000_000.0 + i * 10,
                           "status": "normal", "n": per_window, "readings": [round(rng.gauss(90, 0.9), 2) for _ in range(per_window)]})
    pages = store.con.execute("PRAGMA page_count").fetchone()[0] - store.con.execute("PRAGMA freelist_count").fetchone()[0]
    per = pages * PAGE / sample
    return round(readings / per_window * per * 1.10 / 1024 / 1024, 1)
