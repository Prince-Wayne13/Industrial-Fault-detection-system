---
title: FR-21a
kind: FR
status: not-set
test: inject
scenarios: [Storage fills up]
tags: [requirement, FR]
---

# FR-21a

When storage use reaches 75%, the system shall send an alert to the Administrator only. The Administrator manages storage.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Storage fills up
- **What to do:** Fill storage to 75%.
- **Passes if:** An alert goes to the Administrator only.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
