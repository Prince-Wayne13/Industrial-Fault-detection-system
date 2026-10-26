---
title: NFR-6
kind: NFR
status: not-set
test: inject
injections: [I-10]
tags: [requirement, NFR]
---

# NFR-6

The system shall store at least 99% of the sensor readings its data source generates, including during a connection interruption. The local store records the same readings at the same time as the main store, and the same keep and delete rules apply to both.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[09-demo-control-panel|I-10]] Cut and restore connection
- **Check:** Cut and restore the link. The panel compares readings generated with readings stored. Target 99%.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
