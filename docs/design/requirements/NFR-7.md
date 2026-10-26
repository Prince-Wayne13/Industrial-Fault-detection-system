---
title: NFR-7
kind: NFR
status: not-set
test: inject
scenarios: [Noisy readings]
tags: [requirement, NFR]
---

# NFR-7

The system shall keep producing valid, uncorrupted readings when the input data is noisy or degraded, or shall identify and discard any reading it cannot validate rather than passing it on or acting on it.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Noisy readings
- **What to do:** Play the noisy scenario.
- **Passes if:** Valid readings stay valid. Readings that cannot be checked are thrown away, not acted on.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
