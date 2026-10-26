"""Numbers for the 'measure' tests. Step 10.
NFR-5 uptime, PR-001 status update time, PR-001a alert time, PR-002 dashboard time,
PR-003 10 machines, PR-004 5 users, PR-005 40 readings per second, PR-007 start-up within 60 seconds."""
import time

STARTED = time.time()


def uptime_seconds():
    return time.time() - STARTED
