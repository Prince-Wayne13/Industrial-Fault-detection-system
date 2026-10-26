---
title: NFR-1
kind: NFR
status: not-set
test: inject
injections: [I-17]
tags: [requirement, NFR]
---

# NFR-1

The system shall correctly identify at least 95% of critical faults (temperature and current problems), measured on the labelled simulated test set described in Appendix D.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-17]] Run the labelled test set
- **Check:** Run the labelled set. The panel shows the percentage of critical faults found. Target 95%.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
