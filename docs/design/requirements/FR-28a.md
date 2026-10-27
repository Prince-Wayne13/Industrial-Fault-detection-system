---
title: FR-28a
kind: FR
status: not-set
test: look
scenarios: [Login checks]
tags: [requirement, FR]
---

# FR-28a

Passwords shall be at least 8 characters long, and the system shall accept passwords of 64 characters or more.

## How to test (draft)

- **Method:** look
- **Seeded scenario:** Login checks
- **What to do:** Set a 7-character, an 8-character and a 64-character password.
- **Passes if:** 7 is refused. 8 and 64 are accepted.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
