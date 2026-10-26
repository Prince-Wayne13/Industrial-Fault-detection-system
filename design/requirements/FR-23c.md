---
title: FR-23c
kind: FR
status: not-set
test: inject
injections: [I-02]
tags: [requirement, FR]
---

# FR-23c

A changed limit shall apply to readings received after the change.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-02]] Sustained warning
- **Check:** Change a limit, then replay I-02. The new limit applies to the new readings only.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
