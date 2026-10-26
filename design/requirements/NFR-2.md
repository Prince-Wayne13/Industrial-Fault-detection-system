---
title: NFR-2
kind: NFR
status: not-set
test: inject
injections: [I-17]
tags: [requirement, NFR]
---

# NFR-2

The system shall correctly identify at least 85% of vibration-based faults, measured on the same labelled simulated test set described in Appendix D.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[09-demo-control-panel|I-17]] Run the labelled test set
- **Check:** Run the labelled set. The panel shows the percentage of vibration faults found. Target 85%.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
