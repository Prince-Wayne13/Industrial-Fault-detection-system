---
title: NFR-5
kind: NFR
status: not-set
test: measure
scenarios: [Normal running]
tags: [requirement, NFR]
---

# NFR-5

The system shall keep a record of its own uptime during each test session. During the demonstration, the data-logging function shall be running for at least 95% of the session, not counting planned restarts that the team carries out on purpose (for example, to reload configuration).

## How to test (draft)

- **Method:** measure
- **Seeded scenario:** Normal running
- **What to do:** Read the system's own uptime record for the session.
- **Passes if:** Data logging was running at least 95% of the time.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
