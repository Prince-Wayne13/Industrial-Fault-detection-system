---
title: NFR-8
kind: NFR
status: not-set
test: look
scenarios: [Normal running]
tags: [requirement, NFR]
---

# NFR-8

A user shall be able to see the current status of every piece of monitored equipment from the main dashboard on a single laptop screen, without having to open a second window.

## How to test (draft)

- **Method:** look
- **Seeded scenario:** Normal running
- **What to do:** Open the Overview on one laptop screen.
- **Passes if:** Every machine's status is visible without opening a second window.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
