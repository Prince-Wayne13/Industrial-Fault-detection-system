---
title: Settings
page: 5
status: draft
srs-version: v2.0
roles: [Operator, Engineer, Administrator]
tags: [design, page, industrial-fault-detection]
---

# 5. Settings

Back to [[page-map]]. Previous: [[04-machine-detail]]. Next: [[06-admin]].

One settings page for everyone. It opens from the name side bar in the [[top-bar]]. This page replaces the old Limits page: limits now live here, in a section only Engineers see.

## Layout

```
+------------------------------------------------------------+
| (top bar)                                                  |
+------------------------------------------------------------+
| SETTINGS                                                   |
|                                                            |
| Appearance                                                 |
|   Theme            ( ) Light   (o) Dark                    |
|                                                            |
| Sign-out time                                              |
|   Sign me out after   [ 5 ] minutes idle   (1 to 5)        |
|                                                            |
| Limits                                        Engineer only |
|   Machine type  [ Motor v ]   Parameter [ Temperature v ]  |
|   Warning limit [ 75 ]    Critical limit [ 90 ]            |
|                                          [ Save ]          |
|   Earlier values: 70 / 85, changed 12 Oct 2026             |
+------------------------------------------------------------+
```

## Parts of the page

| Part | What it does | Who | Requirement |
| --- | --- | --- | --- |
| Theme | Switch between light and dark. | everyone | none, see [[srs-changes]] |
| Sign-out time | How long idle before the system signs the person out. Between 1 and 5 minutes. Each person sets their own. The default is 5 minutes. | everyone | [[FR-26]] |
| Limits: choose type and parameter | Pick a machine type and one of its parameters. | Engineer | [[FR-23a]] |
| Limits: warning and critical | Change the warning limit and the critical limit. No restart needed. | Engineer | [[FR-23a]] |
| Limits: check | The warning limit must be lower than the critical limit. If not, the change is refused. | Engineer | [[FR-23b]] |
| Limits: earlier values | The old values and the date of change stay visible. Nothing is overwritten silently. | Engineer | [[FR-23]] |
| Limits: when it applies | A changed limit applies to readings that arrive after the change. Faults already raised keep the limit that was in force. | Engineer | [[FR-23c]], [[FR-23d]] |
| Log entry | Every limit change is also written in the change log on [[06-admin]]. | Engineer | [[FR-22]] |

## Who sees what

| Section | Operator | Engineer | Administrator |
| --- | --- | --- | --- |
| Theme | yes | yes | yes |
| Sign-out time | yes | yes | yes |
| Limits | no | yes | no |

## Open

- [[FR-27]] says configuration is for the Administrator only, but [[FR-23a]] gives limits to the Engineer. The SRS wording needs to say limits are the exception. See [[srs-changes]].
- It is not clear if a limit belongs to a machine type or to each machine on its own. [[FR-23a]] reads as per type. Say so if one machine needs its own limit.
