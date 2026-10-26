---
title: FR-9b
kind: FR
status: not-set
test: inspect
scenarios: [Old data]
tags: [requirement, FR]
---

# FR-9b

The readings of a normal window shall be deleted after 24 hours. The readings of a warning or critical window shall be kept with their status.

## How to test (draft)

- **Method:** inspect
- **Seeded scenario:** Old data
- **What to do:** Load the old data and look at what is kept.
- **Passes if:** Readings of old normal windows are gone. Readings of old warning or critical windows are still there with their status.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
