---
title: FR-8a
kind: FR
status: not-set
test: look
injections: [I-03]
tags: [requirement, FR]
---

# FR-8a

When a fault is acknowledged, the system shall record which user did it and when.

## How it is tested

- **Method:** look (draft)
- **Injection:** [[07-demo-control-panel|I-03]] Sustained critical
- **Check:** After acknowledging, the fault record shows who and when.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
