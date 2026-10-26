---
title: NFR-6
kind: NFR
status: not-set
test: measure
scenarios: [Connection cut]
tags: [requirement, NFR]
---

# NFR-6

The system shall store at least 99% of the sensor readings its data source generates, including during a connection interruption. The local store records the same readings at the same time as the main store, and the same keep and delete rules apply to both.

## How to test (draft)

- **Method:** measure
- **Seeded scenario:** Connection cut
- **What to do:** Compare readings generated with readings stored, including during the cut.
- **Passes if:** At least 99% stored.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
