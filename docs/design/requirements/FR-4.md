---
title: FR-4
kind: FR
status: not-set
test: inject
scenarios: [Sustained warning]
tags: [requirement, FR]
---

# FR-4

The system shall compare incoming measurements against the defined operating limits for the corresponding equipment and parameter and flag measurements or patterns that exceed those limits.

## How to test (draft)

- **Method:** inject
- **Seeded scenario:** Sustained warning
- **What to do:** Play the scenario and watch Motor 1.
- **Passes if:** The high temperature is flagged for Motor 1.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
