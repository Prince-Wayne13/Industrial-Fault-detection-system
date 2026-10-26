---
title: UC-6
kind: UC
tags: [use-case]
---

# UC-6: Place Equipment in Maintenance Mode

**Who:** Engineer

**Goal:** Work on a piece of equipment (for example, testing a pump while it is intentionally run dry) without the system raising false alerts

The full steps are in the SRS. The pages that support this use case show up under Backlinks.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-03]] Sustained critical
- **Check:** Walk the maintenance flow: set maintenance, see readings continue, no alerts, then end it.

