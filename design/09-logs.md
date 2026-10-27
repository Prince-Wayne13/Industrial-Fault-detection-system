---
title: Logs
page: 9
status: draft
srs-version: v2.0
roles: [Administrator]
tags: [design, page, industrial-fault-detection]
---

# 9. Logs

Back to [[page-map]]. Opens from the Logs item in the side menu, or from the link on [[06-admin]]. Administrator only.

The log of who did what and when. It is written in plain sentences, not raw values, and every line is saved in the database. Supports [[FR-22]] and keeps the old limit values that [[FR-23]] asks for.

## Layout

```
+--------------------------------------------------------------------------+
| Logs                                                                       |
| [ All ] [ Limits ] [ Acknowledged ] [ Resolved ] [ Users and machines ]  4 of 4 |
+--------------------------------------------------------------------------+
| When                  Who        What happened               Details      |
| 27 Oct, 12:36:05 PM   operator1  Acknowledged a fault on    FAULT #2 ·   |
|                                  Motor 2                     Temperature  |
| 27 Oct, 12:35:59 PM   engineer1  Changed the vibration       WARNING ABOVE|
|                                  limits of Motor 1           2.8 -> not   |
|                                                              necessary    |
| 27 Oct, 12:35:57 PM   engineer1  Changed the temperature     WARNING ABOVE|
|                                  limits of Motor 1           130 -> 135   |
+--------------------------------------------------------------------------+
```

## Parts of the page

| Part | What it does | Requirement |
| --- | --- | --- |
| Log list | Newest first. One line per action: when, who, what happened in a sentence, and the details as small tags. | [[FR-22]] |
| Limit change tags | Each of the four limits (warning above, critical above, abnormal above, abnormal below) shows as `old -> new`. A limit that did not change is grey, a new one is green, and a limit removed ("not necessary") is red. | [[FR-23]], [[FR-23a]] |
| Acknowledgements | Each person acknowledging a fault is one line: who, the machine, the parameter and the level. The same person acknowledging again does not add a line. | [[FR-8a]], [[FR-22]] |
| Resolved faults | An Engineer resolving a fault is one line. | [[FR-17]] |
| Users and machines | Adding or removing a user, registering or removing a machine. | [[FR-22]], [[UC-5]] |
| Filter | Tabs: All, Limits, Acknowledged, Resolved, Users and machines. A count shows how many lines are listed. | [[FR-22]] |
| Saved in the database | Every line is written to the local database and to the online database, so the log is still there after a restart. | [[FR-22]], [[FR-21]], [[NFR-6]] |

## Who can open it

| Role | Logs page |
| --- | --- |
| Administrator | yes |
| Engineer | no, the page and its menu item are not there |
| Operator | no |

An Engineer who changes a limit sees the result on [[05-settings]] but not the log. The old value is kept in the log. See change 12 in [[srs-changes]].

## Open

- [[FR-23]] says the previous value and the date of change are kept. The log keeps them, but only the Administrator reads it. Does the Engineer also need to see the earlier values? See [[srs-changes]].
- The log has no search and no date filter yet. It shows the latest 500 lines.
