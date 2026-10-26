---
title: Build plan
status: draft
srs-version: v2.0
tags: [design, build-plan]
---

# Build plan

Back to [[page-map]]. The talk that led to this plan is in [[discussions]].

The plan has five segments. The first one is the foundation: it makes the SRS true underneath, with no screens. The other four each give you something you can show.

| Segment | Name | You can show | Requirements made true |
| --- | --- | --- | --- |
| 1 | Foundation | A check script that plays every scenario and prints pass or fail | 52 |
| 2 | Live dashboard | Machine cards with live numbers, status and marks | 2 |
| 3 | Faults you can act on | A pop-up, the bell list, the machine page with history and reports | 3 |
| 4 | People and settings | Sign in, Settings, Admin, Machines list | 1 |
| 5 | Demonstration and proof | The demo panel, the tracker, the measured numbers | 6 |

"Made true" means the requirement now works. "Seen in" (the table at the end) is the segment where you can see it on a screen. A requirement can work in segment 1 and be seen in segment 3.

## What we build with

| Part | Choice |
| --- | --- |
| Back end | Flask (decided, DD-03) |
| Front end | React with JSX (decided, DD-15) |
| Live updates | A live connection from Flask to the dashboard |
| Sensor data | Seed data for everything, including every injection (DC-006) |
| Status model | Threshold screening, then the 10-second trend check, then a logistic regression classifier (DD-05) |
| Local storage | A SQLite file with a set size. When it is full, saving really fails |
| Online database | PostgreSQL if a server is available. If not, a second SQLite file stands in for it and the tracker marks it simulated |
| Passwords | Scrambled with bcrypt |

The folders and the starter files come from `setup.sh` (see [[page-map]] and `SETUP.md`).

---

## Segment 1: Foundation

**Goal.** Every rule in the SRS works behind the scenes. Nothing is drawn yet. If this segment is solid, the rest is putting screens on top.

**Decide before starting** (these blocked the first steps when we checked the SRS):

| # | Decision | Needed by |
| --- | --- | --- |
| 1 | The limits that Appendix A leaves out: motor vibration (warning and critical), motor RPM, pump current, pump RPM, backup power current. [[FR-4]] needs them | 1.3 |
| 2 | What counts as a "physically possible" reading for each parameter ([[FR-14]]) | 1.3 |
| 3 | How much of the 10-second window must be abnormal for a fault ([[FR-6]]). Starting rule: all of it | 1.3 |
| 4 | The size of the local storage file. [[PR-006]] needs room for 3,456,000 readings plus statuses and faults | 1.5 |

**Steps.**

| Step | What | Files | Done when |
| --- | --- | --- | --- |
| 1.1 | Run `setup.sh`. Put the decisions above into `config.py` | config.py | Both parts start |
| 1.2 | Seed data: the machines, one reading per second for every parameter, and the scenario player that can inject each scenario in [[test-plan]] | seed.py, demo.py | A scenario can be played and its readings printed |
| 1.3 | The engine: the reading splits into two streams. The checker keeps bad readings out. The 10-second window collects clean readings. Threshold screening, trend check and status. A silent sensor is flagged after 3 seconds | engine.py, checker.py, model.py | A lone spike gives no fault. A sustained high reading gives a warning, then a critical |
| 1.4 | Faults: one record per abnormal parameter, no repeats while open, each person acknowledges for themselves, only an Engineer resolves, maintenance with a stated time and an overdue flag, the limit in force stored with each fault | faults.py | The whole life of a fault works from the check script |
| 1.5 | Both stores written together. The 24-hour clean-up. The 75% alert. A full local store is caught and logged. Restart carries on | storage.py | Filling the local file to its size triggers the alert, then the full case, with no crash |
| 1.6 | Accounts and roles. Sign-in rules, lockout, sign-out time. The change log. Limits change with the old value and date kept | auth.py, admin.py | A wrong limit is refused. Five wrong passwords block the account |
| 1.7 | The status model trained on a labelled set made from seed data | model.py, seed.py | The accuracy numbers can be read off |
| 1.8 | The check script `check_all.py` plays every scenario and prints pass or fail for each requirement | check_all.py | One command gives the whole table |

**Requirements made true here.** 52 of the 64. The table at the end lists them.

**Show:** run the check script and read the table. This is also the proof that the SRS is met before any screen exists.

---

## Segment 2: Live dashboard

**Goal.** The Overview shows the machines alive.

**Build.** Overview, machine cards, the live connection from Flask, status words, the Sensor fault mark, the Invalid mark, the Maintenance mark, and the "Alerts delayed" notice.

**Files.** Overview.jsx, MachineCard.jsx, api.js, theme.css, app.py (live connection).

**Done when.** On one laptop screen, every machine shows live numbers and a status, and a wrong reading gets its mark without anything breaking ([[NFR-8]], [[PR-002]]).

**Show.** Open the Overview. Play "Normal running", then "Bad reading" and "Sensor goes silent".

---

## Segment 3: Faults you can act on

**Goal.** A fault reaches the right people and can be handled.

**Build.** The fault pop-up that stays until acknowledged, the top bar with the bell list, the machine page (live readings, graph with Day, Week, Month and Year, history, fault list, acknowledge, resolve, maintenance switch), and the report.

**Files.** FaultPopup.jsx, BellList.jsx, TopBar.jsx, MachineDetail.jsx, reports.py.

**Done when.** A fault pops up on an Operator and an Engineer screen, each acknowledges for themselves, the bell count goes down when the Engineer resolves, and a report can be made ([[FR-7]], [[FR-10]]).

**Show.** Play "Sustained warning" with two people signed in.

---

## Segment 4: People and settings

**Goal.** Each role sees and does only what it should.

**Build.** Sign in, the name side bar, Settings (theme, sign-out time, limits for Engineers), Admin (users, machines, storage, change log), and the Machines list.

**Files.** SignIn.jsx, Settings.jsx, Admin.jsx, MachinesList.jsx.

**Done when.** An Operator is turned away from Admin, an Engineer changes a limit with no restart, and the Administrator sees the storage bar and the change log ([[FR-23a]], [[FR-27]]).

**Show.** Play "Login checks" and "Limit change".

---

## Segment 5: Demonstration and proof

**Goal.** Everything can be shown in 5 minutes and every requirement has proof.

**Build.** The demo control panel (near or remote mode, cut the connection, play a scenario), the requirements tracker, the measured numbers (accuracy, speed, load, uptime), the secure connection, and a timed rehearsal of the 5 minutes.

**Files.** DemoPanel.jsx, Tracker.jsx, metrics.py, app.py (certificate).

**Done when.** Every requirement is marked built, simulated or left out, and the 5-minute run has been done twice without stopping ([[FR-11]], [[FR-28e]]).

**Decide before starting.** Which scenarios play live in the 5 minutes, and which are shown as results.

---

## Where every requirement is made true

| Requirement | Made true in | Seen in |
| --- | --- | --- |
| [[FR-1]] | 1 | 2 |
| [[FR-2]] | 1 | 2 |
| [[FR-3]] | 1 | 2 |
| [[FR-3a]] | 1 | 2 |
| [[FR-4]] | 1 | 2 |
| [[FR-5]] | 1 | 2 |
| [[FR-6]] | 1 | 3 |
| [[FR-7]] | 3 | 3 |
| [[FR-7a]] | 3 | 3 |
| [[FR-7b]] | 1 | 3 |
| [[FR-7c]] | 1 | 3 |
| [[FR-8]] | 1 | 3 |
| [[FR-8a]] | 1 | 3 |
| [[FR-8b]] | 1 | 3 |
| [[FR-9]] | 1 | 3 |
| [[FR-9a]] | 1 | 3 |
| [[FR-9b]] | 1 | 3 |
| [[FR-10]] | 3 | 3 |
| [[FR-11]] | 5 | 5 |
| [[FR-12]] | 1 | 5 |
| [[FR-13]] | 1 | 2 |
| [[FR-14]] | 1 | 2 |
| [[FR-15]] | 1 | 3 |
| [[FR-16]] | 1 | 3 |
| [[FR-17]] | 1 | 3 |
| [[FR-18]] | 1 | 3 |
| [[FR-19]] | 1 | 3 |
| [[FR-20]] | 1 | 5 |
| [[FR-21]] | 1 | 5 |
| [[FR-21a]] | 1 | 4 |
| [[FR-22]] | 1 | 4 |
| [[FR-23]] | 1 | 4 |
| [[FR-23a]] | 4 | 4 |
| [[FR-23b]] | 1 | 4 |
| [[FR-23c]] | 1 | 4 |
| [[FR-23d]] | 1 | 3 |
| [[FR-24]] | 1 | 2 |
| [[FR-25]] | 1 | - |
| [[FR-26]] | 1 | 4 |
| [[FR-27]] | 1 | 4 |
| [[FR-28]] | 1 | 4 |
| [[FR-28a]] | 1 | 4 |
| [[FR-28b]] | 1 | 4 |
| [[FR-28c]] | 1 | 4 |
| [[FR-28d]] | 1 | 4 |
| [[FR-28e]] | 5 | 5 |
| [[FR-28f]] | 1 | 5 |
| [[NFR-1]] | 1 | 5 |
| [[NFR-2]] | 1 | 5 |
| [[NFR-5]] | 5 | 5 |
| [[NFR-6]] | 1 | 5 |
| [[NFR-7]] | 1 | 2 |
| [[NFR-8]] | 2 | 2 |
| [[NFR-9]] | 1 | 5 |
| [[NFR-10]] | 1 | 4 |
| [[PR-001]] | 1 | 2 |
| [[PR-001a]] | 1 | 3 |
| [[PR-001b]] | 1 | 3 |
| [[PR-002]] | 2 | 2 |
| [[PR-003]] | 5 | 5 |
| [[PR-004]] | 5 | 5 |
| [[PR-005]] | 1 | 5 |
| [[PR-006]] | 1 | 5 |
| [[PR-007]] | 5 | 5 |
