---
title: NFR-9
kind: NFR
status: not-set
test: inspect
injections: []
tags: [requirement, NFR]
---

# NFR-9

The system shall be built so that the monitoring logic for one equipment type or one parameter can be changed on its own, without needing changes to unrelated parts of the system.

## How it is tested

- **Method:** inspect (draft)
- **Injection:** none
- **Check:** Show the code: monitoring logic for one machine type or parameter lives in its own module.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
