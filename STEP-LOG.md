# Step log

Last updated: 27 Oct 2026 (later). Branch: Design.

## Done

| Segment | What | Delivered | Proof |
| --- | --- | --- | --- |
| 1 Foundation | Engine, faults, storage, accounts, admin, 21 of 22 seeded scenarios, check script, limits references | `fault-detect-segment1.zip` | `check_all.py`: 56 PASS, 0 FAIL |
| 2 Live dashboard | Real-time simulated sensors through the engine, live Overview, machine cards, Sensor fault / Invalid / Maintenance / Overdue marks, "Alerts delayed" notice, demo injection panel | `fault-detect-segment2.zip` | Run once: live numbers, critical status, Invalid mark and Sensor fault mark all showed |
| 3 Faults you can act on | Fault pop-up, bell list, acknowledge per person, Engineer-only resolve, maintenance switch, machine page with graph (Day/Week/Month/Year) and fault history, CSV report, "Act as" picker | `fault-detect-segment3.zip` | Run once over the API: pop-up, Administrator gets none, Operator refused resolve, Engineer resolved, report made, Administrator refused report |
| 4 People and settings | Real sign-in with roles enforced on the server, idle sign-out, name side bar, Settings (sign-out time, password, Engineer limits), Admin (storage, users, machines, change log), Machines page, accounts in the database | `fault-detect-segment4-5.zip` | Run over the API: wrong password refused, Engineer refused Admin, limit change refused then saved, user added, live connection refused without a token |
| 5 Demonstration and proof | Demo page (near/remote, cut/restore, 11 live scenarios, run all checks), requirements tracker, measured numbers, HTTPS | `fault-detect-segment4-5.zip` | Check script: 56 PASS, 0 FAIL. HTTPS served. Heavy load ran 11 machines at 37 readings per second. Link cut kept 41 windows and sent them on restore |
| Follow-up: live window and countdown | Machine page shows each reading of the current 10-second window with its own level, and the last closed window with its status. Demo injections can start after 3 to 15 seconds with a countdown in the corner of every screen, and can be cancelled | `fault-detect-live-window.patch` | Run over the API: spike scheduled 5 s ahead counted down to 0, then showed as one critical reading inside a window that closed Normal |

## Decisions taken so far
- Warning = abnormal for now; wording lives in `frontend/src/status.js` (open item O-10).
- No machine cap in the code; SRS only says at least 10 (O-11).
- A resolved fault never reopens; a new fault is raised if the problem persists.
- Administrator can open a machine page from a card.
- Dark theme later.
- Real sign-in replaced "Act as" (Segment 4).

## Known gaps
- NFR-1 and NFR-2 show 100%: the labelled test set is built from the same limits. Add noisy windows near the limits before the demo.
- PostgreSQL branch is written but not run against a server.
- Sessions and lockout counters are in memory; accounts are in the database.
- "Pump RPM fluctuating" (SRS A.4) is not built, only "below 90%".
- Pump vibration has a gap between 3.0 and 5.0 mm/s; the code treats it as normal.
- Week, Month and Year graphs only show windows that remain after the 24-hour clean-up (FR-9b).
- Any signed-in person can use the Demo page (demo only).
- The Segment 2 and 3 screens were built and run once; no full browser walk-through yet.

## Next

**Before the demo (yours to decide or do)**
- Noisy windows near the limits in the labelled set (NFR-1, NFR-2)
- Two timed 5-minute runs without stopping
- Click through every screen once in a browser, in the three roles
- Settle open items O-10 (warning vs abnormal) and O-11 (machine count)

**Still open in the code**
- Pump RPM fluctuating (SRS A.4); pump vibration gap between 3.0 and 5.0 mm/s
- PostgreSQL run against a real server
- Dark theme
- Sessions and lockout counters survive a restart
