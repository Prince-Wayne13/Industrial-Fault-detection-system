---
title: Discussions
status: draft
srs-version: v2.0
date: 2026-10-26
tags: [design, discussions]
---

# Discussions

Back to [[page-map]].

A record of what we talked about while designing Fault-Detect, and what came out of it. Written on 26 October 2026. The plan that follows from it is [[build-plan]].

## Where we started

- The work is on the branch `v1.7-clear-statements`, which holds version 2.0 of the SRS. The `main` branch still has the older wording, so we use the branch.
- The aim: design the system one step at a time, starting with a page map. Every feature should show which SRS requirement it meets, so we can see what is covered and what is only simulated.
- Notes are written as Obsidian files so they can use graphs and pictures.

## What we decided

### Roles and alerts

- Three roles: Operator, Engineer, Administrator.
- Fault pop-ups go to connected Operators and Engineers only. The Administrator gets no fault pop-ups and does not acknowledge. The storage alert goes to the Administrator only.
- Each person acknowledges a fault for themselves. An Operator acknowledging does not count for the Engineer. See [[fault-popup]].
- The Engineer must acknowledge before resolving. Only an Engineer resolves.
- The Administrator cannot reset passwords. The Administrator can see the Overview, but gets no fault pop-ups.

### Pages

- The pages are: Sign in, Overview, Machine detail, Machines list, Settings, Admin, Demo control panel, and Requirements tracker. See [[page-map]].
- Alerts, History and reports, and Maintenance were folded into other pages: the pop-up, the bell list, and the machine page.
- Page numbers were taken out of the names.
- **Sign in** is simple: the name Fault-Detect, a username box, a password box and one button. See [[sign-in]].
- **Overview** shows every machine as a card in three groups (motors, water pumps, backup power), with live readings, a status mark and a Maintenance mark. See [[overview]].
- **Machine detail** is one page opened from a card, the machines list, or a fault. It has live readings and status, a graph for Day, Week, Month and Year, history, faults, a report button, a maintenance switch and a resolved switch. See [[machine-detail]].
- **Machines list** shows every machine with a filter. See [[machines-list]].
- **Top bar** on every page: the name Fault-Detect, a search bar, a bell, and the person's name. The name opens a side bar with the full name, the role and Settings. See [[top-bar]].
- **Bell list** shows faults the person acknowledged that are not yet resolved. The count drops when an Engineer resolves one.
- **Fault pop-up** stays on screen until that person acknowledges it. It was designed on a canvas with three drawings.
- **Settings** holds the theme (light or dark), each person's sign-out time, and the limits for Engineers. See [[settings]].
- **Admin** has four tabs: Users, Machines, Storage and Change log. See [[admin]].
- Accounts hold a full name. The side bar shows it with the role.

### Look

- The colours are a muted yacht blue with gold. They are in `palette.css` and at the end of [[srs-changes]].
- The suggested use: teal for normal, the muted yellow for warning, red for critical, purple for the Maintenance mark, gold for accents. Status always comes with a word, never colour alone.
- Dark theme colours are not chosen yet.

### The engine

- Every reading splits into two streams. One goes straight to the dashboard, even a wrong one. The other goes to the engine.
- In the engine the checker looks first. A bad reading is logged and kept out. Clean readings go to the status model, which collects 10 seconds and sets the status.
- The SRS (Appendix B) says the flow is threshold screening, then the trend check, then a logistic regression classifier. See [[engine]].

### Storage

- There are two stores written at the same time: an online database and a local store.
- The local store is a SQLite file with a set size, and that size is the "set storage". We tested that such a file really refuses new data when it is full.
- Proposed, not decided: PostgreSQL for the online database. If no server is available, a second file stands in for it and the tracker marks it simulated.
- A button in the demo cuts the link to the online database. The local file keeps everything, and the missing readings are copied across when the link returns.

### Testing and the demonstration

- Build with Flask and React, and use seed data for everything, including every fault injection.
- Every requirement gets a test, in one of four ways: inject, look, inspect or measure. See [[test-plan]].
- The presentation is 5 minutes, so not every scenario can play live.

### How the project is laid out

- Flat on purpose: a `backend` folder and a `frontend` folder, with every file directly inside. `setup.sh` makes them and installs what they need. See `SETUP.md`.

## Changes of mind

| Was | Became |
| --- | --- |
| A separate Limits page | Limits moved into Settings, for Engineers only |
| Alerts, History and Maintenance pages | Folded into the bell list, pop-up and machine page |
| Administrator cannot see the Overview | Administrator can see it, with no fault pop-ups |
| One person acknowledges for everyone | Each person acknowledges for themselves |
| Pages with numbers | Pages with plain names |
| One SQLite database (Appendix B) | An online database and a local store |

The full list, with suggested wording, is in [[srs-changes]].

## Gaps we found in the SRS

- Appendix A has no number for motor vibration, motor RPM, pump current, pump RPM or backup power current, but [[FR-4]] needs defined limits.
- Nothing says what counts as a "physically possible" reading ([[FR-14]]).
- [[FR-6]] does not say how much of the 10 seconds must be abnormal.
- [[FR-27]] says configuration is for the Administrator only, but Engineers change limits ([[FR-23a]]).
- Appendix B (one SQLite database) no longer matches the plan.

## Still open

- Can the Administrator open a machine's page from an Overview card?
- Can a resolved fault be switched back to open?
- **Decided 27 Oct 2026:** limits are maintained per machine. New machines use their type defaults; changing one machine's limits does not change others.
- What colours does the dark theme use?
- Which scenarios play live in the 5 minutes?
- Does the local storage need two sizes, a full one and a small one for the storage demo?
- Where does the link to the Machines list sit?
- The Design branch is not pushed to GitHub yet.

## Files made

| File | What it is |
| --- | --- |
| [[page-map]], `page-map.canvas` | The pages and how they connect |
| [[sign-in]], [[overview]], [[machine-detail]], [[machines-list]], [[settings]], [[admin]] | One note per page |
| [[top-bar]], [[fault-popup]] | Parts shared by every page |
| [[engine]] | How a reading travels |
| [[srs-changes]] | Every change the design asks of the SRS |
| [[test-plan]], `requirements/` | How each requirement is tested, and one small note per requirement |
| [[build-plan]] | The five-segment plan |
| `palette.css` | The colours |
| `setup.sh`, `SETUP.md` | Makes and explains the project |

## How we work

- One step at a time, in plain words, with one question at a time.
- The notes are Obsidian files that also go into the repo.
