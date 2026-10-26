---
title: FR-23c
kind: FR
status: not-set
test: inject
scenarios: [Limit change]
tags: [requirement, FR]
---

# FR-23c

A changed limit shall apply to readings received after the change.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Limit change
- **What to do:** Change a limit, then send readings between the old and new limit.
- **Passes if:** New readings use the new limit. Earlier readings are unchanged.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
