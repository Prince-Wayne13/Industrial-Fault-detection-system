---
title: FR-7c
kind: FR
status: not-set
test: inject
injections: [I-03]
tags: [requirement, FR]
---

# FR-7c

If no Operator or Engineer is connected, the fault shall stay open and be shown to the next Operator or Engineer who connects.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-03]] Sustained critical
- **Check:** Run I-03 with nobody signed in as Operator or Engineer. Sign in afterwards: the open fault is shown.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
