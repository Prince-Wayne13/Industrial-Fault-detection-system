---
title: FR-7
kind: FR
status: not-set
test: inject
injections: [I-03]
tags: [requirement, FR]
---

# FR-7

When the status model confirms a fault, the system shall show a pop-up alert to every connected Operator and Engineer, whether near-range or remote.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-03]] Sustained critical
- **Check:** Run I-03 with an Operator and an Engineer signed in on two screens. Both get the pop-up.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
