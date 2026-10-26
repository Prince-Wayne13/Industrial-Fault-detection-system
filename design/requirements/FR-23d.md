---
title: FR-23d
kind: FR
status: not-set
test: look
injections: [I-02]
tags: [requirement, FR]
---

# FR-23d

Each fault record shall store the limit that was in force when the fault was raised.

## How it is tested

- **Method:** look (draft)
- **Injection:** [[07-demo-control-panel|I-02]] Sustained warning
- **Check:** Open the fault record raised after a limit change. It shows the limit in force at that time.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
