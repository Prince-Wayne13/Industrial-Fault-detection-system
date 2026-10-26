---
title: NFR-5
kind: NFR
status: not-set
test: look
injections: [I-13]
tags: [requirement, NFR]
---

# NFR-5

The system shall keep a record of its own uptime during each test session. During the demonstration, the data-logging function shall be running for at least 95% of the session, not counting planned restarts that the team carries out on purpose (for example, to reload configuration).

## How it is tested

- **Method:** look (draft)
- **Injection:** [[07-demo-control-panel|I-13]] Restart the system
- **Check:** The panel shows logging uptime for the session. A planned restart (I-13) is not counted.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
