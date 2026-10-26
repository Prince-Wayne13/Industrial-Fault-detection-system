---
title: FR-7c
kind: FR
status: not-set
test: inject
scenarios: [Nobody connected]
tags: [requirement, FR]
---

# FR-7c

If no Operator or Engineer is connected, the fault shall stay open and be shown to the next Operator or Engineer who connects.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Nobody connected
- **What to do:** Play the scenario with nobody signed in, then sign in as an Operator.
- **Passes if:** The fault is still open and its pop-up appears.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
