---
title: NFR-9
kind: NFR
status: not-set
test: inspect
scenarios: [Normal running]
tags: [requirement, NFR]
---

# NFR-9

The system shall be built so that the monitoring logic for one equipment type or one parameter can be changed on its own, without needing changes to unrelated parts of the system.

## How to test (draft)

- **Method:** inspect
- **Seeded scenario:** Normal running
- **What to do:** Show the code for one parameter's logic, then change it.
- **Passes if:** Only that part changes. Nothing unrelated needs editing.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
