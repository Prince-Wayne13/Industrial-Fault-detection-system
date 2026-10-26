---
title: FR-21a
kind: FR
status: not-set
test: inject
injections: [I-12]
tags: [requirement, FR]
---

# FR-21a

When storage use reaches 75%, the system shall send an alert to the Administrator only. The Administrator manages storage.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[09-demo-control-panel|I-12]] Fill storage
- **Check:** Push storage to 75% while signed in as the Administrator. Only the Administrator's bell shows the alert.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
