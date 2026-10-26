---
title: FR-3a
kind: FR
status: not-set
test: measure
scenarios: [Normal running]
tags: [requirement, FR]
---

# FR-3a

The system shall take one reading per second for every monitored parameter on every machine.

## How to test (draft)

- **Method:** measure
- **Seeded scenario:** Normal running
- **What to do:** Count the readings for one parameter over one minute.
- **Passes if:** About 60 readings, one each second, for every parameter.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
