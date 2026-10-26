---
title: FR-4
kind: FR
status: not-set
test: inject
injections: [I-02]
tags: [requirement, FR]
---

# FR-4

The system shall compare incoming measurements against the defined operating limits for the corresponding equipment and parameter and flag measurements or patterns that exceed those limits.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-02]] Sustained warning
- **Check:** Run I-02. The reading is flagged once it passes the limit.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
