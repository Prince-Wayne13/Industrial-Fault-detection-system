# Segment 1: Foundation

Put the contents of this folder over the repo (branch `Design`). It replaces files in `system/backend/` and adds
`docs/design/limits-references.md`.

## Run it

```
cd system/backend
pip install -r requirements.txt
python check_all.py
```

One table, PASS or FAIL for each requirement, and a copy in `check_report.md`. The last run: 56 PASS, 0 FAIL, 8 shown in later segments.

## What each file does (plan steps 1.1 to 1.8)

| File | Step | What it does |
| --- | --- | --- |
| `config.py` | 1.1 | Every number. The four open decisions are filled (limits, possible readings, 100% trend rule, 512 MB file). Limits have references. |
| `clock.py` | 1.1 | The one time source (FR-25). Can be fixed or fast-forwarded for scenarios. |
| `seed.py`, `demo.py` | 1.2 | Machines, readings, and all 22 scenario names. 21 play; "Near and remote mode" is Segment 5. |
| `checker.py`, `engine.py`, `model.py` | 1.3, 1.7 | Two streams, bad-reading checker, 10-second window, trend check, logistic-regression classifier. |
| `faults.py` | 1.4 | Fault life: open, acknowledge per person, resolve, maintenance, overdue, delayed-alert flag. |
| `storage.py` | 1.5 | Local file with a real size cap, online database, 24-hour clean-up, 75% alert, full-store and cut-link handling. |
| `auth.py`, `admin.py` | 1.6 | Roles, passwords, lockout, sessions, change log, limit changes. |
| `system.py` | | Wires all of it together. The Flask app in Segment 2 uses this class. |
| `metrics.py` | 1.8 | Storage projection for PR-006. |
| `check_all.py` | 1.8 | The check script. |

`app.py` and `reports.py` are unchanged (Segments 2 and 3).

## Decisions taken so that the work could continue (change any of them in `config.py`)

1. Parameters with one abnormal level have two statuses: normal and abnormal. The rest have three.
2. Missing limits filled from the sources in `docs/design/limits-references.md`.
3. Physically possible ranges: see `PHYSICAL_RANGE`.
4. A fault needs the whole 10-second window abnormal (`TREND_FRACTION = 1.0`).
5. Local file is 512 MB; about 45 MB is needed for one day at the minimum load.
6. A limit belongs to a machine type, not to one machine.
7. A worse level on an already-open fault updates the same record and makes no second pop-up (FR-16).
8. During maintenance, new fault alerts are held back and logged, and stay held back after the time runs out (the machine shows overdue) until the Engineer ends maintenance.

## Known gaps

- The online database branch for PostgreSQL is written but has not been run against a server. The checks use the second SQLite file that stands in for it.
- Accounts are kept in memory. They survive a planned restart in the demo, not a real process restart. Move them to the database in Segment 4.
- NFR-1 and NFR-2 show 100% because the labelled set is built from the same limits it is tested against. The test only becomes hard when the set has noisy windows close to the limits. Add those before the demo if you want a number the examiners will trust.
- Pump RPM "fluctuating" is not built (see the references note).
