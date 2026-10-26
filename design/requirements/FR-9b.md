---
title: FR-9b
kind: FR
status: not-set
test: inject
injections: [I-14]
tags: [requirement, FR]
---

# FR-9b

The readings of a normal window shall be deleted after 24 hours. The readings of a warning or critical window shall be kept with their status.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-14]] Fast-forward the clock
- **Check:** Fast-forward 24 hours. Normal readings are gone; warning and critical readings are still there.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
