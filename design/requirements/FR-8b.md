---
title: FR-8b
kind: FR
status: not-set
test: look
injections: [I-03]
tags: [requirement, FR]
---

# FR-8b

Acknowledging shall not close the fault. It stays open until an Engineer marks it resolved (FR-17).

## How it is tested

- **Method:** look (draft)
- **Injection:** [[07-demo-control-panel|I-03]] Sustained critical
- **Check:** After acknowledging, the fault is still open.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
