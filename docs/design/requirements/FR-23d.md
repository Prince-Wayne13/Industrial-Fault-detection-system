---
title: FR-23d
kind: FR
status: not-set
test: inject
scenarios: [Limit change]
tags: [requirement, FR]
---

# FR-23d

Each fault record shall store the limit that was in force when the fault was raised.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Limit change
- **What to do:** Raise a fault, change the limit, then open the fault.
- **Passes if:** The fault shows the limit that was in force when it was raised.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
