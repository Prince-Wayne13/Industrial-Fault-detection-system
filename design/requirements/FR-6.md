---
title: FR-6
kind: FR
status: not-set
test: inject
injections: [I-01, I-02]
tags: [requirement, FR]
---

# FR-6

A condition flagged by FR-4 shall not be classified as a fault under FR-5 based on a single abnormal reading alone. The system shall first check whether the abnormal condition holds across the readings of the latest 10-second window for that parameter; only if it does shall FR-5 classification and the FR-7 alert proceed. A single abnormal reading that does not repeat is not treated as a fault, and the dashboard's live reading (see NFR-8) is unaffected either way.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-01]] One-off blip, [[07-demo-control-panel|I-02]] Sustained warning
- **Check:** Run I-01: no fault, no alert, the live number still moves. Then run I-02: the fault is raised only after the window.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
