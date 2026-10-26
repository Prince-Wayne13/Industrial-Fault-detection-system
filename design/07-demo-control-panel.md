---
title: Demo control panel
page: 7
status: draft
srs-version: v2.0
roles: [demonstration only]
tags: [design, page, demo, industrial-fault-detection]
---

# 7. Demo control panel

Back to [[page-map]]. Previous: [[06-admin]]. Next: [[08-requirements-tracker]].

The page the team uses during the 5-minute presentation. It does one job: let the examiners see every requirement proven. Supports [[UC-4]], [[FR-11]] and [[FR-12]], and carries the injections for the rest. DC-006 says the demonstration is a dashboard plus fault injection.

## The seed-data rule

- Nothing on the panel is random. Every injection replays a **seeded scenario**: a fixed file of readings and timings. It gives the same result every time, which a 5-minute slot needs.
- The seeded readings must still travel through the real Flask back end and out to the React dashboard. They must not be painted straight onto the screen. If they were, the timing requirements ([[PR-001]], [[PR-001a]], [[PR-002]]) would prove nothing.
- The labelled seed set for [[NFR-1]] and [[NFR-2]] holds the true answer for each case, so the panel can score itself.

## How each requirement is proven

| Way | Meaning |
| --- | --- |
| Inject | Press a button on the panel and watch the result. |
| Look | Check something on screen: a mark, a colour, a refusal. |
| Inspect | Show it in the settings or the code. It cannot be triggered by a button. |

Draft count over the 70 requirement notes: 34 inject, 30 look, 6 inspect. Each requirement note now has a `test` line and a "How it is tested" section. They are drafts for the team to review.

## Layout

```
+--------------------------------------------------------------------+
| DEMO CONTROL PANEL (demonstration only)        Demo clock 14:02:11 |
+--------------------------------------------------------------------+
| CONNECTION   (o) Near   ( ) Remote     [ Cut link ] [ Restore ]    |
+--------------------------------------------------------------------+
| FAULT INJECTION        Machine [ Motor 1 v ]  Parameter [ Temp v ] |
|  [I-01 Blip] [I-02 Warning] [I-03 Critical] [I-04 Vibration]       |
|  [I-05 Two at once] [I-06 Hold and repeat] [I-07 Silent sensor]    |
|  [I-08 Bad reading] [I-09 Noise]                                   |
+--------------------------------------------------------------------+
| SYSTEM                                                             |
|  [I-11 Delay alert] [I-12 Fill storage 75% | full | down]          |
|  [I-13 Restart] [I-15 Load up] [I-16 5 viewers]                    |
|  [I-14 Fast-forward: 15 min | 1 h | 24 h]                           |
+--------------------------------------------------------------------+
| SCORING   [I-17 Run labelled set]  Critical 96%   Vibration 88%    |
+--------------------------------------------------------------------+
| LIVE READOUTS (tag)                                                |
|  Reading to screen   0.4 s   (PR-002)   Status every  10 s (PR-001)|
|  Status to alert     0.8 s   (PR-001a)  Readings/s      42 (PR-005)|
|  Generated 1,204  Stored 1,204  (NFR-6) Logging uptime 99% (NFR-5) |
|  Time to monitoring 31 s     (PR-007)                              |
+--------------------------------------------------------------------+
| Open: [ Requirements tracker ]                                     |
+--------------------------------------------------------------------+
```

- Every button carries its injection number, for example `I-03`, and the requirement tags it proves.
- The live readouts exist so that Look requirements such as [[PR-001]] and [[PR-002]] show a number, not a claim.
- The demo clock exists so that the 24-hour, 15-minute lockout and maintenance-overdue cases do not need real waiting.
- Look requirements (passwords, roles, limits, history) need no button. The tracker tells the presenter where to look.

## The injections (draft names)

The detail of each injection, its seed file and its timing is to be agreed later. The table shows only what each one proves.

| ID | Name | What it does | Proves |
| --- | --- | --- | --- |
| I-01 | One-off blip | One reading jumps out of range once, then goes back. | [[FR-6]] |
| I-02 | Sustained warning | A parameter stays past its warning limit for longer than 10 seconds. | [[FR-4]], [[FR-5]], [[FR-6]], [[FR-23c]], [[FR-23d]] |
| I-03 | Sustained critical | A parameter stays past its critical limit for longer than 10 seconds. | [[FR-5]], [[FR-7]], [[FR-7a]], [[FR-7b]], [[FR-7c]], [[FR-8]], [[FR-8a]], [[FR-8b]], [[FR-9]], [[FR-17]], [[FR-18]], [[PR-001a]], [[UC-2]], [[UC-6]] |
| I-04 | Vibration fault | Vibration rises into a fault pattern. |  |
| I-05 | Two at once | Two parameters on one machine go abnormal together. | [[FR-15]] |
| I-06 | Hold and repeat | Keep a fault going while it is open, then return to normal and trigger it again. | [[FR-16]] |
| I-07 | Sensor goes silent | One parameter stops sending for 3 seconds or more. | [[FR-13]] |
| I-08 | Bad reading | Send a reading of the wrong type, a missing value, and an impossible value. | [[FR-14]], [[NFR-7]] |
| I-09 | Noisy signal | Add noise to a stream of normal readings. | [[NFR-7]] |
| I-10 | Cut and restore connection | Switch near or remote mode, cut the link, restore it. | [[FR-11]], [[FR-12]], [[NFR-6]], [[UC-4]] |
| I-11 | Delay the alert | Hold an alert back by more than 2 seconds. | [[PR-001b]] |
| I-12 | Fill storage | Push storage to 75%, then full, then unavailable. | [[FR-20]], [[FR-21a]], [[NFR-10]] |
| I-13 | Restart the system | Stop and restart the back end, as a planned restart. | [[FR-21]], [[NFR-5]], [[PR-007]] |
| I-14 | Fast-forward the clock | Jump the demo clock: 24 hours, past a maintenance time, past a lockout, past an idle time. | [[FR-9b]], [[FR-19]], [[FR-26]], [[FR-28d]], [[NFR-10]] |
| I-15 | Load up | Add machines and extra parameters up to 10 machines and beyond. | [[PR-003]], [[PR-005]] |
| I-16 | Extra viewers | Open 5 dashboard sessions at the same time. | [[PR-004]] |
| I-17 | Run the labelled test set | Replay the labelled seeded set and show the percentage found. | [[NFR-1]], [[NFR-2]] |

## Requirements with no injection

These are proven by looking or by inspecting. The tracker lists them with the same lines.

| Requirement | Way | Check |
| --- | --- | --- |
| [[FR-1]] | look | Overview shows temperature, current, vibration and RPM on each motor card. |
| [[FR-2]] | look | Overview shows bearing temperature, current, vibration and RPM on each pump card. |
| [[FR-3]] | look | Overview shows internal temperature, current and fan speed on each UPS card. |
| [[FR-3a]] | look | The panel's reading counter shows 1 reading per second per parameter. |
| [[FR-9a]] | inspect | Show the stored status and time stamp for each 10-second window in the Storage tab. |
| [[FR-10]] | look | Open the history on a machine page. Generate a report as Operator or Engineer. |
| [[FR-22]] | look | Make a user, machine and limit change. The Change log tab shows who and when. |
| [[FR-23]] | look | Change a limit in Settings. The change log keeps the old value and the date. |
| [[FR-23a]] | look | Change a limit as an Engineer from Settings. No restart. |
| [[FR-23b]] | look | Try a warning limit at or above the critical limit. It is refused. |
| [[FR-24]] | look | Overview shows several motors as separate cards, each with its own status and history. |
| [[FR-25]] | inspect | Show the single time source in the code and that panel timestamps agree across components. |
| [[FR-27]] | look | Sign in as Operator and as Engineer and try the Admin page. It is refused. The Engineer can still change limits. |
| [[FR-28]] | look | Open any page while signed out. It sends you to sign in. |
| [[FR-28a]] | look | Try a 14-character password (refused) and a 64-character one (accepted). |
| [[FR-28b]] | look | Set a password with no capitals, numbers or symbols. It is accepted. No change is forced. |
| [[FR-28c]] | look | Try a password from the common list. It is refused. |
| [[FR-28e]] | inspect | Show the HTTPS connection and the TLS version in the browser. |
| [[FR-28f]] | inspect | Show the user table: only salted hashes, no readable passwords. |
| [[NFR-8]] | look | All machines are visible on the Overview on one laptop screen. |
| [[NFR-9]] | inspect | Show the code: monitoring logic for one machine type or parameter lives in its own module. |
| [[PR-001]] | look | The panel shows the time between status updates. It stays at 10 seconds or less. |
| [[PR-002]] | look | The panel shows the time from reading received to reading on screen. 2 seconds or less. |
| [[PR-006]] | inspect | Show the storage size and the sum: 10 x 4 x 86,400 = 3,456,000 readings a day. |
| [[UC-1]] | look | Sign in and open the Overview. Pick a machine. |
| [[UC-3]] | look | Pick a machine, choose a period, view the graph and the report. |
| [[UC-5]] | look | As Administrator, add, change and remove a user and a machine. |

## Who sees this page

Demonstration only. It is not a product page and has no requirement of its own. It is not part of the role table. It opens from the tracker or by its own address.

## Open

- Whether the presenter runs the injections by hand or one button runs a scripted 5-minute sequence. Not decided.
- The agreed injection details: seed files, exact limits and timings.
- Whether I-15 really adds machines or replays a seeded load.
- FR-25 (one time source) and FR-28e (HTTPS) need the demo to run over HTTPS. Check that the demo laptop setup allows it.
