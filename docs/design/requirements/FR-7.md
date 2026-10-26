---
title: FR-7
kind: FR
status: not-set
test: inject
scenarios: [Sustained warning]
tags: [requirement, FR]
---

# FR-7

When the status model confirms a fault, the system shall show a pop-up alert to every connected Operator and Engineer, whether near-range or remote.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Sustained warning
- **What to do:** Play the scenario with an Operator and an Engineer signed in, one near and one remote.
- **Passes if:** A pop-up appears on both screens.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
