---
title: NFR-10
kind: NFR
status: not-set
test: inject
injections: [I-12, I-14]
tags: [requirement, NFR]
---

# NFR-10

The system shall keep statuses and warning or critical records until storage use reaches 75%, and shall never delete them automatically. The readings of normal windows are deleted after 24 hours (FR-9b).

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-12]] Fill storage, [[07-demo-control-panel|I-14]] Fast-forward the clock
- **Check:** Fast-forward 24 hours: normal readings go, statuses and warning or critical records stay. Fill storage to 75%: still nothing deleted by the system.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
