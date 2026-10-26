---
title: NFR-7
kind: NFR
status: not-set
test: inject
injections: [I-08, I-09]
tags: [requirement, NFR]
---

# NFR-7

The system shall keep producing valid, uncorrupted readings when the input data is noisy or degraded, or shall identify and discard any reading it cannot validate rather than passing it on or acting on it.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-08]] Bad reading, [[07-demo-control-panel|I-09]] Noisy signal
- **Check:** Run I-09 and I-08. Valid readings stay valid, unusable readings are discarded.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
