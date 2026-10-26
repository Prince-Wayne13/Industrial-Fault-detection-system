---
title: FR-6
kind: FR
status: not-set
test: inject
scenarios: [Lone spike]
tags: [requirement, FR]
---

# FR-6

A condition flagged by FR-4 shall not be classified as a fault under FR-5 based on a single abnormal reading alone. The system shall first check whether the abnormal condition holds across the readings of the latest 10-second window for that parameter; only if it does shall FR-5 classification and the FR-7 alert proceed. A single abnormal reading that does not repeat is not treated as a fault, and the dashboard's live reading (see NFR-8) is unaffected either way.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Lone spike
- **What to do:** Play the lone spike.
- **Passes if:** No fault is raised from one reading. A fault only appears when it lasts across the 10-second check.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
