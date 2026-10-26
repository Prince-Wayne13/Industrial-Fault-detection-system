---
title: NFR-2
kind: NFR
status: not-set
test: measure
scenarios: [Labelled test set]
tags: [requirement, NFR]
---

# NFR-2

The system shall correctly identify at least 85% of vibration-based faults, measured on the same labelled simulated test set described in Appendix D.

## How to test (draft)

- **Method:** measure
- **Seeded scenario:** Labelled test set
- **What to do:** Run the labelled set and count vibration faults found.
- **Passes if:** At least 85% found.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
