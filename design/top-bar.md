---
title: Top bar
status: draft
srs-version: v2.0
roles: [Operator, Engineer, Administrator]
tags: [design, shared, industrial-fault-detection]
---

# Top bar and name side bar

Back to [[page-map]].

Shown at the top of every page after [[01-sign-in]]. It is the same everywhere, so it is written once here.

## Layout

```
+------------------------------------------------------------+
| Fault-Detect    [ Search machines ...... ]   (bell 3)  Name v |
+------------------------------------------------------------+
```

When the name is clicked, a side bar slides in from the right:

```
                          +----------------------+
                          |  Full name           |
                          |  Role                |
                          |  Settings            |
                          +----------------------+
```

## Parts

| Part | What it does | Requirement |
| --- | --- | --- |
| Software name | Fault-Detect, on the left. Click to go home. | none |
| Search bar | Finds a machine by its name and opens it. | none |
| Bell icon | A number on it counts faults that are acknowledged and not yet resolved. Click it to open a small window listing them. | [[srs-changes]], change 3 |
| Bell list | Each line is one fault. Choosing it opens that machine's [[04-machine-detail]]. When the Engineer resolves a fault, it leaves the list and the number goes down. | [[FR-17]] |
| Fault pop-up | Separate from the bell. See [[fault-popup]]. | [[FR-7]], [[FR-7a]], [[FR-7c]] |
| Name, top right | The signed-in person's name. Click it to open the side bar. | none |
| Side bar | Shows the full name and the role, and a Settings link that opens [[05-settings]]. | none |

## Who sees what in the bell

| Role | The bell shows |
| --- | --- |
| Operator | the faults they acknowledged that are not resolved yet |
| Engineer | the faults they acknowledged that are not resolved yet |
| Administrator | no fault alerts ([[FR-7b]]); the storage alert only ([[FR-21a]]) |

## Open

- Search is set to find machines by name. Nothing in the SRS asks for search, so this is a design choice and the tracker will show it as extra.
- The SRS does not say an account has a full name. It only says the Administrator manages accounts ([[UC-5]]). If the side bar shows a full name, the SRS needs one line saying accounts hold it.
- Whether the Administrator's bell shows the storage alert as a number or only on [[06-admin]] is not decided.
