---
title: FR-23b
kind: FR
status: not-set
test: inject
scenarios: [Limit change]
tags: [requirement, FR]
---

# FR-23b

The system shall reject a new limit if the warning limit is not below the critical limit.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Limit change
- **What to do:** Try a warning limit that is not below the critical limit.
- **Passes if:** The change is refused.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
