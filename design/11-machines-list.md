---
title: Machines list
page: 11
status: draft
srs-version: v2.0
roles: [Operator, Engineer]
tags: [design, page, industrial-fault-detection]
---

# 11. Machines list

Back to [[page-map]]. The number 11 only means it was added later. It is not the order of use.

A list of every registered machine, with a filter. It is not the same as machine registration on [[08-admin]], which is where the Administrator adds machines.

## Layout

```
+------------------------------------------------------------+
| (top bar)                                                  |
+------------------------------------------------------------+
| Machines     Type [ All v ]   Status [ All v ]             |
+------------------------------------------------------------+
| Name     | Type       | Status    | Open faults | Mark      |
| Motor 1  | Motor      | Warning   | 2           |           |
| Motor 2  | Motor      | Normal    | 0           | MAINT.    |
| Pump 1   | Water pump | Normal    | 0           |           |
| UPS 1    | Backup power | Critical | 1          |           |
+------------------------------------------------------------+
```

Choosing a row opens [[03-machine-detail]], the same page that opens from a card on the [[02-overview]].

## Parts of the page

| Part | What it does | Requirement |
| --- | --- | --- |
| List of all machines | Every registered machine, each on its own line with its own status. | [[FR-24]], [[FR-5]] |
| Filter | Narrows the list by machine type or by status. | none |
| Maintenance mark | Shown while a machine is in maintenance mode. | [[FR-18]], [[FR-19]] |
| Open faults count | How many faults of that machine are not resolved yet. | [[FR-17]] |
| Row click | Opens the machine's page. | [[UC-1]] step 3 |

## Open

- You said "filter per machine". I made it a filter by type and by status, plus the search bar in the [[top-bar]] for a name. Say so if you meant something else.
- Where the link to this page sits (top bar or elsewhere) is not decided.
- Filter is a design choice, not in the SRS. The tracker shows it as extra.
