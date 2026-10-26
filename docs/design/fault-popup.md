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

## The design

Drawn on a canvas you can open and comment on: https://claude.ai/artifact/Pa7Tw4dYXM7536t3B5kFFz

It has three drawings: a warning, a critical fault, and two pop-ups on screen at once.

| Part | What it looks like |
| --- | --- |
| Box | A paper-coloured card (`--bg-card`) with a thin edge (`--border-light`), rounded corners and a soft shadow so it sits above the page. 440 px wide. |
| Level tag | A small pill at the top left. A coloured dot and the word WARNING or CRITICAL. The colour is `--warning` or `--red`, and the word always comes with it. |
| Time | Top right, for example 10:42:07. |
| Machine name | The biggest text in the box, for example Motor 1. |
| What is wrong | One plain line, for example "Temperature is too high." |
| The numbers | The reading now and the limit it passed. |
| Acknowledge button | Dark yacht blue (`--primary`), the main button. |
| Open machine button | A quiet outlined button that opens that machine's [[machine-detail]]. |
| Reminder line | "Stays on your screen until you acknowledge it." |

When two faults arrive, the pop-ups stack in the corner, newest on top. Each one is acknowledged on its own.

The example machines and numbers in the drawings are only samples.

### Added by the design

- The "Open machine" button is not in the SRS and you did not ask for it. It saves one click, and the tracker will show it as extra.
- The numbers line (reading and limit) is not in the SRS wording of [[FR-7a]]. Say so if you would rather leave it out.
