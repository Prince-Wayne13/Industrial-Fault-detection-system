---
title: FR-8b
kind: FR
status: not-set
test: look
scenarios: [Sustained warning]
tags: [requirement, FR]
---

# FR-8b

Acknowledging shall not close the fault. It stays open until an Engineer marks it resolved (FR-17).

## How to test (draft)

- **Method:** look
- **Seeded scenario:** Sustained warning
- **What to do:** After acknowledging, look at the fault again.
- **Passes if:** It is still open, not resolved.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
