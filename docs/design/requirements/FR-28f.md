---
title: FR-28f
kind: FR
status: not-set
test: inspect
scenarios: [Login checks]
tags: [requirement, FR]
---

# FR-28f

The system shall store passwords only in a salted, hashed form that cannot be read back.

## How to test (draft)

- **Method:** inspect
- **Seeded scenario:** Login checks
- **What to do:** Look at how a password is stored.
- **Passes if:** It is scrambled and cannot be read back.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
