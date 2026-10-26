---
title: FR-5
kind: FR
status: not-set
test: inject
scenarios: [Sustained warning, Sustained critical]
tags: [requirement, FR]
---

# FR-5

For conditions flagged by FR-4, the system shall classify the condition as normal, warning, or critical using the defined fault-classification method and identify the affected equipment and parameter. Where the limits define only one abnormal level, the system shall classify the condition as normal or abnormal.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Sustained warning, Sustained critical
- **What to do:** Play both scenarios.
- **Passes if:** The status shows warning, then critical, naming the machine and parameter.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
