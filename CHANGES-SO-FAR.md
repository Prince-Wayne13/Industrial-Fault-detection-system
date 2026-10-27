# Changes so far (Design branch)

Apply from the repo root: `git apply all-changes.patch` (includes the earlier UI shell merge). Needs `pip install bcrypt flask-socketio` for the back end.

## 1. UI
- New frame merged earlier (side nav, top bar, panels, pop-up stack).
- Fault pop-up now shows the reading and the limit: "Temperature is too high. 140 °C now. Limit is 130 °C." Low limits say "too low". Speed swings say "swinging up and down".
- Older pages (Machines, Machine, Settings, Admin, Demo, Tracker, Sign in) restyled through the theme: pill-style status tags, new buttons, inputs, tables.
- Lint: 25 warnings down to 4, 0 errors. Build passes.

## 2. Gaps closed
- Fault record now carries `value` and `reason`.
- Pump RPM "fluctuating" (SRS A.4) built: the median step between neighbouring readings in the 10-second window above 6% of the mean. One spike or one ramp never triggers it (FR-6). Limit in `config.py` as `fluctuation_step`.
- Demo: new "Pump speed swings" scenario (Demo page, live) and a `fluctuate` action.
- Pump vibration gap 3.0 to 5.0 mm/s: decided as no status between them, one abnormal level at 5.0. Cross-checked against Europump guidance (3.0 / 5.5 / 7.1 mm/s). Wording for A.4 is in `docs/design/segment data/limits-references.md`, with reference R7.
- NFR-1 and NFR-2: 640 noisy windows added to the labelled set (near-limit normal, near-limit fault, brief crossings, swinging speed, noisy normal). Result: 3,200 of 3,200 windows right, critical temperature and current 160 of 160, vibration 240 of 240, on four different random seeds. It stays at 100% because every window is labelled by how it was built, with at least a 1% margin from the limit. Say that to the lecturer; do not present it as field accuracy.
- Check script: 56 PASS, 0 FAIL. FR-6 now also proves the pump-speed rule, FR-7a proves the pop-up carries value and limit.

## 3. Demo preparation
- `demo-click-through.md`: every screen, three roles, tick boxes.
- O-10 and O-11 have proposed SRS wording in `docs/open-items.md` (Owner and Date still empty: your group decides).
- Two timed 5-minute runs: running now, results follow.
