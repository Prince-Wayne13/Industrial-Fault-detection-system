---
title: Build plan
status: draft
srs-version: v2.0
tags: [design, build-plan]
---

# Build plan

Back to [[page-map]].

Rebuilt after checking every requirement in SRS v2.0. All 64 requirements have a place to be built. The table at the end shows where, and the plan below shows the order.

## What we are building with

| Part | Choice |
| --- | --- |
| Back end | Flask (decided, DD-03) |
| Front end | React with JSX (decided, DD-15) |
| Live updates | A live connection from Flask to the dashboard, so readings arrive without refreshing |
| Sensor data | Seed data for everything, including every injection (DC-006) |
| Status model | Threshold screening, then the 10-second trend check, then a logistic regression classifier (DD-05, Appendix B) |
| Local storage | A SQLite file with a set size. When it is full, saving really fails |
| Online database | PostgreSQL if a server is available. If not, a second SQLite file stands in for it, and the tracker marks it simulated |
| Passwords | Scrambled with bcrypt, never stored in readable form |

## The project folders

Only two new folders, and each file sits straight inside it.

```
Industrial-Fault-detection-system/
  setup.sh            makes everything below
  SETUP.md            how to run it, step by step
  srs/                the requirements (already there)
  docs/               the discussion notes and the Obsidian design notes (already there)
  backend/            Flask: one file per job, no sub-folders
    app.py  config.py  checker.py  model.py  engine.py  faults.py
    storage.py  auth.py  admin.py  reports.py  seed.py  demo.py  metrics.py
  frontend/           React: one file per page or part, no sub-folders
    src/  App.jsx  main.jsx  api.js  theme.css  TopBar.jsx
          SignIn.jsx  Overview.jsx  MachinesList.jsx  MachineDetail.jsx
          Settings.jsx  Admin.jsx  DemoPanel.jsx  Tracker.jsx
          FaultPopup.jsx  BellList.jsx  MachineCard.jsx
```

## The order of work

One step at a time. Each step ends with something you can see working.

| Step | What | You see | Requirements |
| --- | --- | --- | --- |
| 1 | Run `setup.sh` | A blank Fault-Detect opens in the browser | none |
| 2 | Seed machines and one reading per second | Cards with live numbers on the Overview | FR-1 to FR-3, FR-3a, FR-24, NFR-8 |
| 3 | Two streams and the checker | Wrong readings get an Invalid mark. A silent sensor shows Sensor fault | FR-13, FR-14, NFR-7, PR-002 |
| 4 | Threshold screening, trend check, status | Normal, warning or critical on each card | FR-4 to FR-6, PR-001 |
| 5 | Faults, pop-up, bell list | A pop-up that stays until acknowledged | FR-7 to FR-8b, FR-15 to FR-17 |
| 6 | Both stores, 75% alert, full store | The storage bar and the alert | FR-9a, FR-9b, FR-12, FR-20, FR-21, FR-21a, NFR-6, NFR-10 |
| 7 | Sign in, roles, settings, admin | Login, lockout, limits, change log | FR-22 to FR-23c, FR-26 to FR-28f |
| 8 | Maintenance, graphs, reports | Machine detail with Day, Week, Month, Year | FR-9, FR-10, FR-18, FR-19 |
| 9 | Demo panel and tracker | The scenarios play from buttons | FR-11 |
| 10 | Measure and finish | Accuracy, speed, load, uptime, secure connection | NFR-1, NFR-2, NFR-5, NFR-9, PR-003 to PR-007, FR-28e |

## Things the SRS does not say yet

These came up while checking. Each one blocks a step, so they need an answer before that step.

| # | Gap | Blocks |
| --- | --- | --- |
| 1 | [[FR-4]] needs defined limits, but Appendix A has no number for: motor vibration warning and critical (only "per ISO 10816-3"), motor RPM, pump current, pump RPM and backup power current | Step 4 |
| 2 | [[FR-14]] needs a "physically possible" range for each parameter. The SRS gives none. `config.py` has placeholders | Step 3 |
| 3 | [[FR-6]] says an abnormal condition must "hold across" the 10 seconds. How much of the window must be abnormal is not stated. Was "all of it"; now the trained model scores each window and 50% or more flags it. See [[engine]] | Step 4 |
| 4 | Appendix B says one SQLite database. The new plan has an online database and a local one. See [[srs-changes]], changes 11 and 12 | Step 6 |
| 5 | The size of the local storage file. [[PR-006]] needs room for 3,456,000 readings plus statuses and faults, so the real size has to be measured | Step 6 |
| 6 | The logistic regression needs a labelled set to learn from. It will be made from seed data (Appendix D) | Step 10 |
| 7 | A secure connection ([[FR-28e]]) on a laptop needs a local certificate. If it is skipped, the tracker marks it simulated | Step 10 |
| 8 | Which scenarios play live in the 5 minutes | Step 9 |

## Where every requirement is built

| Requirement | Built in | Screens | Step |
| --- | --- | --- | --- |
| [[FR-1]] | seed.py | Overview, MachineCard, MachinesList | 2 |
| [[FR-2]] | seed.py | Overview, MachineCard, MachinesList | 2 |
| [[FR-3]] | seed.py | Overview, MachineCard, MachinesList | 2 |
| [[FR-3a]] | engine.py | Overview | 3 |
| [[FR-4]] | model.py, engine.py | MachineCard | 4 |
| [[FR-5]] | model.py, engine.py | MachineCard | 4 |
| [[FR-6]] | model.py, engine.py | MachineCard | 4 |
| [[FR-7]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-7a]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-7b]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-7c]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-8]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-8a]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-8b]] | faults.py | BellList, MachineDetail | 5 |
| [[FR-9]] | reports.py | MachineDetail | 8 |
| [[FR-9a]] | storage.py | Admin | 6 |
| [[FR-9b]] | storage.py | Admin | 6 |
| [[FR-10]] | reports.py | MachineDetail | 8 |
| [[FR-11]] | demo.py | DemoPanel | 9 |
| [[FR-12]] | storage.py | Admin | 6 |
| [[FR-13]] | engine.py | Overview, MachineCard | 3 |
| [[FR-14]] | checker.py | Overview, MachineCard | 3 |
| [[FR-15]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-16]] | faults.py | FaultPopup, TopBar | 5 |
| [[FR-17]] | faults.py | BellList, MachineDetail | 5 |
| [[FR-18]] | faults.py | MachineCard, MachineDetail | 8 |
| [[FR-19]] | faults.py | MachineCard, MachineDetail | 8 |
| [[FR-20]] | storage.py | Admin | 6 |
| [[FR-21]] | storage.py | Admin | 6 |
| [[FR-21a]] | storage.py | Admin | 6 |
| [[FR-22]] | admin.py | Settings, Admin | 7 |
| [[FR-23]] | admin.py | Settings, Admin | 7 |
| [[FR-23a]] | admin.py | Settings, Admin | 7 |
| [[FR-23b]] | admin.py | Settings, Admin | 7 |
| [[FR-23c]] | admin.py | Settings, Admin | 7 |
| [[FR-23d]] | faults.py | BellList, MachineDetail | 5 |
| [[FR-24]] | seed.py | Overview, MachineCard, MachinesList | 2 |
| [[FR-25]] | engine.py | Overview | 3 |
| [[FR-26]] | auth.py | SignIn, Settings | 7 |
| [[FR-27]] | auth.py | SignIn, Settings | 7 |
| [[FR-28]] | auth.py | SignIn, Settings | 7 |
| [[FR-28a]] | auth.py | SignIn, Settings | 7 |
| [[FR-28b]] | auth.py | SignIn, Settings | 7 |
| [[FR-28c]] | auth.py | SignIn, Settings | 7 |
| [[FR-28d]] | auth.py | SignIn, Settings | 7 |
| [[FR-28e]] | app.py (certificate) | - | 10 |
| [[FR-28f]] | auth.py | SignIn, Settings | 7 |
| [[NFR-1]] | model.py | - | 10 |
| [[NFR-2]] | model.py | - | 10 |
| [[NFR-5]] | metrics.py | - | 10 |
| [[NFR-6]] | storage.py | Admin | 6 |
| [[NFR-7]] | checker.py | Overview, MachineCard | 3 |
| [[NFR-8]] | - | Overview | 2 |
| [[NFR-9]] | model.py (one file per parameter) | - | 10 |
| [[NFR-10]] | storage.py | Admin | 6 |
| [[PR-001]] | model.py, engine.py | MachineCard | 4 |
| [[PR-001a]] | engine.py, faults.py | FaultPopup | 5 |
| [[PR-001b]] | engine.py, faults.py | FaultPopup | 5 |
| [[PR-002]] | engine.py | Overview | 3 |
| [[PR-003]] | metrics.py, app.py | - | 10 |
| [[PR-004]] | metrics.py, app.py | - | 10 |
| [[PR-005]] | engine.py | Overview | 3 |
| [[PR-006]] | storage.py | Admin | 6 |
| [[PR-007]] | metrics.py | - | 10 |
