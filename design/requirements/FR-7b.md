---
title: FR-7b
kind: FR
status: not-set
test: look
injections: [I-03]
tags: [requirement, FR]
---

# FR-7b

The system shall not send fault alerts to the Administrator.

## How it is tested

- **Method:** look (draft)
- **Injection:** [[09-demo-control-panel|I-03]] Sustained critical
- **Check:** Keep an Administrator signed in during I-03. No pop-up reaches them.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
