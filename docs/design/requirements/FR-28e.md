---
title: FR-28e
kind: FR
status: not-set
test: inspect
scenarios: [Login checks]
tags: [requirement, FR]
---

# FR-28e

All communication between the dashboard and the server shall use HTTPS (TLS 1.2 or newer).

## How to test (draft)

- **Method:** inspect
- **Seeded scenario:** Login checks
- **What to do:** Look at the address and the connection details in the browser.
- **Passes if:** It uses https with TLS 1.2 or newer.

Status is one of: built, simulated, left-out, not-set. Change the `status` line above.

The pages that cover this requirement show up under Backlinks.
