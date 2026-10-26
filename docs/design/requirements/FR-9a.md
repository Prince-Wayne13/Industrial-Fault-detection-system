---
title: FR-9a
kind: FR
status: not-set
test: inspect
scenarios: [Normal running]
tags: [requirement, FR]
---

# FR-9a

For every 10-second window, the system shall store the status and its time stamp.

## How to test (draft)

- **Method:** inspect
- **Seeded scenario:** Normal running
- **What to do:** Look at the stored statuses in the database.
- **Passes if:** One status with a time for every 10 seconds.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
