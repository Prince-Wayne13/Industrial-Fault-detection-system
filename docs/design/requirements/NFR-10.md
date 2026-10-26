---
title: NFR-10
kind: NFR
status: not-set
test: inspect
scenarios: [Storage fills up]
tags: [requirement, NFR]
---

# NFR-10

The system shall keep statuses and warning or critical records until storage use reaches 75%, and shall never delete them automatically. The readings of normal windows are deleted after 24 hours (FR-9b).

## How to test (draft)

- **Method:** inspect
- **Seeded scenario:** Storage fills up
- **What to do:** Look at stored statuses and warning or critical records as storage grows.
- **Passes if:** Nothing is deleted automatically before 75% is reached. Normal readings still go after 24 hours.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
