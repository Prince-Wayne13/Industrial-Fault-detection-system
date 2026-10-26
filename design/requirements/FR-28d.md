---
title: FR-28d
kind: FR
status: not-set
test: inject
injections: [I-14]
tags: [requirement, FR]
---

# FR-28d

After 5 failed login attempts on an account, the system should block login to that account for 15 minutes.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-14]] Fast-forward the clock
- **Check:** Fail 5 logins. The account is blocked. Fast-forward 15 minutes and it opens again.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
