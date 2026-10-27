# Check report: Segment 1

| Requirement | Result | What was checked | Detail |
| --- | --- | --- | --- |
| FR-1 | PASS | Motor shows temperature, current, vibration, RPM | 4 parameters on every motor |
| FR-2 | PASS | Pump shows bearing temperature, current, vibration, RPM | 4 parameters |
| FR-3 | PASS | UPS shows internal temperature, current, fan speed | 3 parameters |
| FR-3a | PASS | One reading per second per parameter | 61 seconds gave 61 readings per parameter (60 stored, 1 in the open window) |
| FR-4 | PASS | A sustained high reading is flagged | Motor 1 temperature flagged |
| FR-5 | PASS | Warning, critical, and abnormal where only one level exists | motor temperature/current/vibration have 3 statuses; pump temperature, rpm, UPS and others have 2 |
| FR-6 | PASS | One abnormal reading is never a fault | spike: no fault. Sustained: fault only when the 10-second window ended. Pump speed swing: abnormal; one low reading: none |
| FR-7 | PASS | Pop-up for every connected Operator and Engineer | both see it (screen in Segment 3) |
| FR-7a | PASS | Pop-up carries machine, parameter, type, level, time | all fields present, including the reading and the limit (screen in Segment 3) |
| FR-7b | PASS | Administrator gets no fault alerts | no pop-up, no bell list |
| FR-7c | PASS | Nobody connected: fault stays open and is shown to the next person | shown when the Operator connects |
| FR-8 | PASS | Each person acknowledges for themselves | Operator's pop-up goes, Engineer's stays |
| FR-8a | PASS | Acknowledging records who and when | operator1 |
| FR-8b | PASS | Acknowledging does not close the fault | still open; shows in the bell list |
| FR-9 | PASS | Faults and readings can be called up | fault history and the 10 readings of the warning window |
| FR-9a | PASS | Every 10-second window keeps its status and time | 6 windows in 60 seconds, 10 seconds apart |
| FR-9b | PASS | Normal readings go after 24 hours; warning and critical stay | 5 old normal windows cleared, statuses all kept, warning/critical readings kept |
| FR-10 | SEGMENT 3 | history and report on the machine page |  |
| FR-11 | SEGMENT 5 | Bluetooth / Wi-Fi mode on the demo panel |  |
| FR-12 | PASS | Connection cut: keep collecting, send on restore | 38 windows held locally and sent on restore |
| FR-13 | PASS | Silent sensor flagged within 3 seconds | dashboard shows a sensor fault, not the last number |
| FR-14 | PASS | Wrong type, missing and impossible readings are rejected and logged | 3 rejected, logged, system carried on |
| FR-15 | PASS | One fault record per abnormal parameter | 2 records |
| FR-16 | PASS | No second alert while a fault is open | 1 record while open, a new one only after it was resolved and came back |
| FR-17 | PASS | Only an Engineer resolves, after acknowledging; time recorded | Operator refused, Engineer needs to acknowledge first, bell count drops |
| FR-18 | PASS | Maintenance mode: readings and alerts paused | no readings or alerts while the machine is in maintenance |
| FR-19 | PASS | Overdue maintenance is flagged | Motor 1 overdue after its stated minute |
| FR-20 | PASS | Storage full: keep readings, no crash, event logged | 59 windows in temporary storage |
| FR-21 | PASS | Restart: last settings and open faults come back | limit 135 kept, fault kept, status back after fresh readings |
| FR-21a | PASS | Storage alert at 75% goes to the Administrator only | alert at 75% |
| FR-22 | PASS | Change log: who and when | engineer1 changed the limit |
| FR-23 | PASS | Old value and date kept when a limit changes | 130 kept next to 135 |
| FR-23a | PASS | Engineer changes a limit, no restart | works; Operator refused (screen in Segment 4) |
| FR-23b | PASS | Warning limit must stay below critical | The warning limit must be below the critical limit. |
| FR-23c | PASS | A new limit applies to later readings only | 132 was a warning at 130, normal at 135; old windows unchanged |
| FR-23d | PASS | Each fault stores the limit in force when it was raised | fault shows 130 although the limit is now 135 |
| FR-24 | PASS | Several machines of one type are separate units | Motor 1 faulted; Motors 2 and 3 untouched |
| FR-25 | FAIL | One time source | ['soak.py'] |
| FR-26 | PASS | Sign-out time 1 to 5 minutes, own setting | 1 and 5 accepted, 6 refused, idle session expired |
| FR-27 | PASS | Administrator-only functions | Operator/Engineer refused; Administrator allowed; no password reset exists |
| FR-28 | PASS | Sign in first | no session -> sign-in page |
| FR-28a | PASS | Passwords: 7 refused, 8 and 64 accepted | ok |
| FR-28b | PASS | No forced mix of characters | all-lowercase accepted |
| FR-28c | PASS | Common passwords refused | That password is too common. |
| FR-28d | PASS | 5 wrong passwords block the account for 15 minutes | Too many wrong passwords. The account is blocked for 15 minutes. |
| FR-28e | SEGMENT 5 | HTTPS certificate |  |
| FR-28f | PASS | Passwords stored salted and scrambled | bcrypt, different every time |
| NFR-1 | PASS | At least 95% of critical temperature and current faults found | 160 of 160 = 100% |
| NFR-2 | PASS | At least 85% of vibration faults found | 240 of 240 = 100% |
| NFR-5 | SEGMENT 5 | uptime measured over the demo |  |
| NFR-6 | PASS | At least 99% of readings stored, also during a cut | generated 589, local 589, online 589 |
| NFR-7 | PASS | Noisy data: no corrupt reading acted on | noise at 3x raises no fault; bad readings never enter a window |
| NFR-8 | SEGMENT 2 | all machines on one screen |  |
| NFR-9 | PASS | One parameter's logic changes on its own | only motor vibration changed |
| NFR-10 | PASS | Nothing deleted automatically before 75% | every window saved so far is still there |
| PR-001 | PASS | Status updates at least every 10 seconds | every 10 seconds |
| PR-001a | PASS | Critical alert within 2 seconds of the status | 0.0 s |
| PR-001b | PASS | A late alert is still shown, logged and flagged | alert came after 3.0 s: shown, logged, 'alerts delayed' set |
| PR-002 | SEGMENT 2 | reading to screen within 2 seconds |  |
| PR-003 | PASS | 10 machines at the same time | 10 machines, status every 10 s (screen timing in Segment 5) |
| PR-004 | SEGMENT 5 | 5 viewers at once |  |
| PR-005 | PASS | At least 40 readings per second | 184,573 readings per second processed |
| PR-006 | PASS | Room for 3,456,000 readings plus statuses and faults | about 45.3 MB needed for one day; the local file is set to 512 MB |
| PR-007 | SEGMENT 5 | start-up within 60 seconds |  |

55 PASS, 1 FAIL, 8 to be shown in later segments
