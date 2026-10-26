---
title: NFR-1
kind: NFR
status: not-set
test: measure
scenarios: [Labelled test set]
tags: [requirement, NFR]
---

# NFR-1

The system shall correctly identify at least 95% of critical faults (temperature and current problems), measured on the labelled simulated test set described in Appendix D.

## How to test (draft)

- **Method:** measure
- **Seeded scenario:** Labelled test set
- **What to do:** Run the labelled set and count critical temperature and current faults found.
- **Passes if:** At least 95% found.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
