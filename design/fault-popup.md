---
title: Fault pop-up
status: draft
srs-version: v2.0
roles: [Operator, Engineer]
tags: [design, shared, industrial-fault-detection]
---

# Fault pop-up

Back to [[page-map]].

The box that appears on screen when a fault is confirmed. It is shared by every page, so it is written once here.

```
+----------------------------------+
|  WARNING     Motor 1             |
|  Temperature too high            |
|  10:42:07                        |
|                    [Acknowledge] |
+----------------------------------+
```

| Rule | Requirement |
| --- | --- |
| Appears for every connected Operator and Engineer, near or remote. Never for the Administrator. | [[FR-7]], [[FR-7b]] |
| Shows the machine, the parameter, the fault type, the level and the time. | [[FR-7a]] |
| Stays on screen until that person acknowledges it. | [[srs-changes]], change 2 |
| Each person acknowledges for themselves. An Operator acknowledging does not clear the Engineer's pop-up. | [[srs-changes]], change 1 |
| Acknowledging records who did it and when, and moves the fault into that person's bell list. | [[FR-8a]] |
| If nobody is connected, the fault stays open and is shown to the next Operator or Engineer who connects. | [[FR-7c]] |
| A fault already open does not make a second pop-up. | [[FR-16]] |
