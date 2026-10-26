---
title: UC-4
kind: UC
tags: [use-case]
---

# UC-4: Continue Monitoring During a Connection Interruption

**Who:** System (initiated automatically)

**Goal:** Keep collecting and showing equipment data even when the connection between system components is temporarily lost

The full steps are in the SRS. The pages that support this use case show up under Backlinks.

## How it is tested

- **Method:** inject (draft)
- **Injection:** [[07-demo-control-panel|I-10]] Cut and restore connection
- **Check:** Run the connection flow from the panel: near, remote, cut, restore. Watch the Bluetooth and Wi-Fi icons in the top bar follow each step.

