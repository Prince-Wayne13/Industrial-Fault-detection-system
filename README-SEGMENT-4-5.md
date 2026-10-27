# Segments 4 and 5: people, settings, demonstration and proof

Unzip over the repo (Design branch). Then:

    cd system/backend && pip install -r requirements.txt && python app.py
    cd system/frontend && npm install && npm run dev

Open the Vite address. Sign in with a demo account (Demo accounts on the sign-in page). Delete `system/backend/local_store.db`
and `online_store.db` first if you want a clean start.

HTTPS (FR-28e): start the server with `HTTPS=adhoc python app.py` (self-made certificate, the browser warns once), or set
`SSL_CERT` and `SSL_KEY` to a real certificate. Start Vite with `BACKEND=https://127.0.0.1:5000 npm run dev`.

## Segment 4: people and settings
- Real sign-in replaces "Act as". The token is checked on every call, and the role is enforced on the server, not only on screen.
- The live connection also needs a signed-in token.
- Sign-out after the person's own idle time (1 to 5 minutes). Only the person's own activity keeps the session alive; live data does not.
- Name side bar: full name, role, Settings, Sign out.
- Settings: sign-out time, change own password, Engineer-only limits table with change history. The theme is light only (dark later).
- Admin (Administrator only): storage bar with the alert level, users, machines, change log.
- Machines page (Operator, Engineer): filter by type and status, open fault count.
- Accounts are saved in the database, so they survive a restart.

## Segment 5: demonstration and proof
- Demo page: near range (Bluetooth) or remote range (Wi-Fi) mode, cut and restore the connection, 11 scenarios played live,
  manual injection, "Run all checks" for the scenarios shown as results.
- Tracker page: every requirement as built, simulated, left out or not set, with the last check result, and the measured numbers
  (accuracy, alert time, reading time, machines, viewers, readings per second, storage, start-up time, uptime).
- `tracker_status.json` holds the status notes that the check script cannot decide (FR-11, FR-12, NFR-5 simulated; others built).
- Check script: 56 PASS, 0 FAIL. FR-25 failed once on the way (new files read the computer clock); fixed with `clock.real()`.

## Decisions taken
- Live scenarios: normal running, lone spike, sustained warning, sustained critical, two faults at once, sensor goes silent,
  bad reading, maintenance, slow alert, connection cut, heavy load. Shown as results: storage fills up, storage fails, restart,
  fault returns, limit change, nobody connected, noisy readings, labelled test set, login checks, old data.
- Near and remote mode only change the label and the top bar chip. Both show the same data (the pass rule of FR-11).
- Cutting the connection stops saving to the online database only. Collecting and showing carry on (FR-12). Restoring sends what waited.
- Each browser tab is its own sign-in, so two people can be shown on one laptop.
- Any signed-in person may use the Demo page. The 5-minute run is easiest from an Administrator tab.
- The Administrator cannot reset passwords; each person changes their own.

## Before the demo
- Add noisy windows near the limits to the labelled set, or NFR-1 and NFR-2 stay at an easy 100%.
- Time the 5-minute run twice without stopping.
- Run "Run all checks" once on the demo laptop so the Tracker shows fresh results (about 100 seconds).
- Open 5 tabs to show PR-004 (viewers on the Tracker page).

## Known gaps
- Lockout counters and sessions are in memory; a server restart signs everyone out.
- The PostgreSQL branch is still not run against a server.
- "Pump RPM fluctuating" (SRS A.4) is still not built. Pump vibration still has the 3.0 to 5.0 mm/s gap.
- Uptime (NFR-5) is measured for the demo session only.
- Screens were built and checked through the API and a build; no full click-through in a browser yet.
- Open items O-10 (warning vs abnormal wording) and O-11 (machine count) are still open.
