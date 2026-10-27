# Segment 3: faults you can act on

Unzip over the repo (Design branch). Run as in Segment 2 (`python app.py`, `npm run dev`).

## Show
Open the Demo page, make Motor 1 temperature a warning value, wait about 10 seconds. Use the "Act as" picker in the top bar
to switch between Operator, Engineer and Administrator.

- Operator and Engineer get the pop-up; the Administrator never does. Each acknowledges for themselves; the fault stays open.
- Acknowledged faults appear in that person's bell. Only an Engineer resolves (on the machine page); the bell count then drops.
- Machine page: live readings, graph (Day, Week, Month, Year), fault history, maintenance switch (Engineer), Generate report (Operator, Engineer; CSV).

## Decisions taken
- "Act as" stands in for sign-in until Segment 4. The API trusts the user name sent with each call. Not secure; for the demo only.
- A pop-up is any open fault the person has not acknowledged, so a person who opens the app later still gets it (FR-7c).
- A resolved fault does not reopen. If the problem is still there, the next window raises a new fault.
- Week, Month and Year graphs show only the windows that remain, because normal readings go after 24 hours (FR-9b).
- The report is a CSV: performance per parameter, the faults, and faults that recurred.
- Administrator's bell shows the storage alert count only (FR-7b, FR-21a).
