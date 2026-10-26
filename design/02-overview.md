---
title: Overview
page: 2
status: draft
srs-version: v2.0
roles: [Operator, Engineer, Administrator]
tags: [design, page, industrial-fault-detection]
---

# 2. Overview

Back to [[page-map]]. Previous: [[01-sign-in]]. Next: [[03-machines-list]].

The main screen. It answers one question: is everything fine right now? Supports [[UC-1]].

## Layout

The top bar is shared by every page. It is described in [[top-bar]].

```
+------------------------------------------------------------+
| Fault-Detect   [ Search ......... ]   (bell 2)   Name v    |
+------------------------------------------------------------+
| (notice bar: "Alerts delayed" shows only when needed)      |
+------------------------------------------------------------+
| MOTORS                                                     |
| +----------------+ +----------------+                      |
| | Motor 1        | | Motor 2        |                      |
| | [ NORMAL ]     | | [ WARNING ]    |                      |
| | Temp   62 C    | | Temp   81 C    |                      |
| | Current 4.1 A  | | Current 4.0 A  |                      |
| | Vibration ok   | | Vibration high |                      |
| | RPM    1480    | | RPM    1475    |                      |
| +----------------+ +----------------+                      |
| +----------------+                                         |
| | Motor 3        |                                         |
| | [ NORMAL ]     |                                         |
| | MAINTENANCE    |   <- mark when in maintenance mode      |
| | Temp   40 C ...|                                         |
| +----------------+                                         |
|                                                            |
| WATER PUMPS                                                |
| +----------------+                                         |
| | Pump 1  ...    |                                         |
| +----------------+                                         |
|                                                            |
| BACKUP POWER                                               |
| +----------------+                                         |
| | UPS 1   ...    |                                         |
| +----------------+                                         |
+------------------------------------------------------------+
```

- Every registered machine is on this page, each as its own card.
- Each card shows the live readings and the status as a mark.
- Choosing a card, for example Motor 1, opens [[04-machine-detail]]. That page shows that machine's readings, status, history and faults.
- A card in maintenance mode carries a "Maintenance" mark.
- The status is shown with a word and a colour, never colour alone.

## Parts of the page

| Part | What it shows | Requirement |
| --- | --- | --- |
| Top bar | Search, bell for alerts, name with side bar. See [[top-bar]]. | [[FR-7]] |
| Motors group | Temperature, current, vibration and speed (RPM) for each motor. | [[FR-1]] |
| Water pumps group | Bearing temperature, current, vibration and speed (RPM) for each pump. | [[FR-2]] |
| Backup power group | Internal temperature, charging or output current and cooling fan speed for each unit. | [[FR-3]] |
| One card per machine | Each machine is separate, with its own status. Several machines of one type can sit side by side. | [[FR-24]] |
| Status mark on each card | Normal, warning or critical. Machines with only one abnormal level show normal or abnormal. | [[FR-5]] |
| Status refresh | The card status updates at least every 10 seconds. | [[PR-001]] |
| Live numbers | A new reading appears on the card within 2 seconds. | [[PR-002]] |
| "Sensor fault" mark | If a parameter sends nothing for 3 seconds, its number is replaced by this mark. An old number is never shown as current. | [[FR-13]] |
| "Invalid" mark | A wrong, missing or impossible reading is kept out of the status check and logged. | [[FR-14]] |
| "Maintenance" mark | Shown while a machine is in maintenance mode. Readings keep coming, new fault alerts pause. | [[FR-18]] |
| "Overdue" mark | Shown when a machine stays in maintenance past its stated time. | [[FR-19]] |
| "Alerts delayed" notice | Appears at the top only when an alert came more than 2 seconds late. | [[PR-001b]] |
| Empty message | If no machine is registered, a clear message is shown instead of a blank screen. | [[UC-1]] step 2a |

Readings are taken once a second for every parameter on every machine ([[FR-3a]]). The card shows them as they arrive, so the numbers move faster than the status word.

## Who sees this page

| Role | Sees it |
| --- | --- |
| Operator | yes |
| Engineer | yes |
| Administrator | yes, to look. No fault pop-ups. The bell carries the storage alert only. |

## Use case steps

| Step in [[UC-1]] | On this page |
| --- | --- |
| 1. The user opens the dashboard. | This page opens after [[01-sign-in]]. |
| 2. The system shows the status of every machine. | The cards. |
| 3. The user picks a machine. | Click a card. |
| 4. The system shows the readings and recent history. | Opens [[04-machine-detail]]. |

## Open

- Whether the Administrator can open a machine's page from a card is not decided.
- Cards or one single list: cards are the choice for now.
