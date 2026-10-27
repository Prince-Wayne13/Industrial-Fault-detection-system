# Segment 2: live dashboard

Unzip over the repo (Design branch). Then:

    cd system/backend && python app.py          # server, port 5000
    cd system/frontend && npm install && npm run dev

Open the Vite address. The Overview shows every machine with live numbers. Open **Demo** in the top bar to inject
a warning or critical value, a bad reading, a silent sensor, maintenance mode or slow alerts.

## What changed
- `backend/live.py` (new): real-time simulated sensors through the real engine. Readings go out at once (`reading`),
  statuses go out when a window closes (`status`) and are saved by the engine, a snapshot goes out each second (`overview`).
- `backend/app.py`: starts the feed; `/api/overview`, `/api/demo`, socket events. Uses real files `local_store.db` and `online_store.db`
  (delete them to start clean).
- `frontend`: `Overview`, `MachineCard`, `DemoPanel`, `useLive.js`, `status.js`, `TopBar` (Demo link), `theme.css`.

## Decisions taken
- Warning = abnormal for now. Both words exist; wording lives in `status.js` (open item O-10).
- A card opens the machine page for every role, the Administrator too.
- A resolved fault does not reopen; a return of the problem is a new fault.
- No cap on machines in the code. The SRS gives only "at least 10" (PR-003). Flagged for review (O-11).
- Dark theme later. Sign-in is Segment 4, so the demo endpoint has no login yet.

## Not in this segment
Fault pop-up, bell, machine page content (Segment 3). Sign-in and roles on screen (Segment 4).
