# Live window and injection countdown

Apply `fault-detect-live-window.patch` on top of Segments 4 and 5. No new packages.

## What you see
- **Machine page, "Window and graph":** pick a parameter. "This 10-second window" shows one tile per second as the readings arrive,
  each with its own level (Normal, Warning/Abnormal, Critical, as a word and a colour). Under it, "Last window" shows the ten readings
  of the window that just closed and the status it got. A single high reading shows as one flagged tile while the window stays Normal.
- **Demo page, "Start in":** choose Now, 3, 5, 7, 10 or 15 seconds. The injection does not start at once. A card in the bottom-right
  corner of every signed-in screen counts down ("Starts in 5 s", 4, 3, ...), then shows "Started". Cancel removes it before it starts.
  Reset, mode changes and Cancel are always immediate.

## How the status is decided (for the examiners)
1. Each reading is screened against the limits (FR-4).
2. When the 10 seconds end, the trend check asks how much of the window was over a limit. Today the whole window must be (`TREND_FRACTION = 1.0` in `config.py`). One reading never flags a window (FR-6).
3. Only a flagged window goes to the logistic regression classifier, which assigns warning or critical (DD-05). If scikit-learn is missing the rule level is used.

## Changed
`live.py` (window readings, last window, level of each reading, scheduled injections), `app.py` (delay and cancel, trend fraction on `/api/limits`),
frontend: `LiveWindow.jsx` and `InjectionTimer.jsx` (new), `MachineDetail.jsx`, `DemoPanel.jsx`, `App.jsx`, `useLive.js`, `theme.css`.
