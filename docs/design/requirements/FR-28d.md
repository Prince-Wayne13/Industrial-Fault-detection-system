---
title: FR-28d
kind: FR
status: not-set
test: look
scenarios: [Login checks]
tags: [requirement, FR]
---

# FR-28d

After 5 failed login attempts on an account, the system should block login to that account for 15 minutes.

## How to test (draft)

- **Method:** look
- **Seeded scenario:** Login checks
- **What to do:** Enter a wrong password 5 times.
- **Passes if:** The account is blocked for 15 minutes and the message says so.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
