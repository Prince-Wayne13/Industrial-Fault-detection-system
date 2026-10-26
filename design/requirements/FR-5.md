---
title: FR-5
kind: FR
status: not-set
test: inject
injections: [I-02, I-03]
tags: [requirement, FR]
---

# FR-5

For conditions flagged by FR-4, the system shall classify the condition as normal, warning, or critical using the defined fault-classification method and identify the affected equipment and parameter. Where the limits define only one abnormal level, the system shall classify the condition as normal or abnormal.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-02]] Sustained warning, [[07-demo-control-panel|I-03]] Sustained critical
- **Check:** Run I-02 for warning and I-03 for critical. The card shows the status, machine and parameter. Repeat on a machine with one abnormal level.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
