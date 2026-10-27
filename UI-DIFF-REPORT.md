# UI shell merge: what went in, what did not

Branch: Design. Source: the uploaded UI files (mock-data shell) against `system/frontend/src` (live, Segments 1 to 5 per STEP-LOG.md).
Build: `vite build` passes, lint 0 errors. Not browser-tested.

## Rule used
The repo is the live, working system, so it wins on data and logic (`user.jsx`, `useFaults.js`, `useLive.js`, `api.js`, `status.js`, all pages). The upload wins on look and frame. Anything that only existed to fake data was left out.

## Added to the repo (new files)
SideNav, Layout, NamePanel, ConnectionIcons, Pill, PopupStack, Icons, format.js, connection.js (linkWord only is used)

## Replaced with the new look, wired to live data
| File | Change |
| --- | --- |
| TopBar | Search (still jumps to the machine), connection icons, bell with count, person button opens NamePanel |
| BellList | Popover; live faults; Administrator sees the storage alert only |
| FaultPopup + PopupStack | Approved stacked bottom-right design; Acknowledge calls the server; "Open machine" link; Administrator gets none (server decides) |
| MachineCard | New card; keeps Overdue, Invalid, Sensor fault, Maintenance marks |
| Overview | Five summary tiles + grouped cards; keeps lost-connection, link-cut and Alerts-delayed notices |
| App | Signed pages now sit inside Layout |
| theme.css | New theme first, then the old rules for pages not yet redesigned; bell count renamed `.bell-badge` so it no longer clashes with the status `.badge`; injection countdown moved bottom-left so it does not sit on the pop-ups |

## NOT added (UI in the upload that is not in the final project)
| Upload item | Why left out |
| --- | --- |
| `AppContext.jsx`, `useApp.js`, `mockData.js` | Stand-in data. Replaced by `user.jsx`, `useFaults.js`, `useLive.js` |
| "Demonstration tools" in the name panel: role switcher | Real sign-in replaced "Act as" (Segment 4) |
| "Send a test fault pop-up" button | Faults come from the engine; the Demo page injects real ones |
| "Work Bluetooth in range" / "Wi-Fi available" checkboxes | Backend has no such state. Near/Remote and Cut/Restore are on the Demo page |
| Connection mode menu (Automatic / Bluetooth only / Wi-Fi only) and the "Switched to Wi-Fi" note | Backend knows only `near` / `remote` and link up/cut. **Decision for you:** add automatic switching to the backend, or drop it from `design/top-bar.md` |
| Manual-mode dot on the icons | Goes with the mode menu |
| Pop-up line "138 °C now. Warning limit is 130 °C." | Fault record carries the limit but not the live value; pop-up shows the limit only. Add `value` to the fault payload to restore it |
| Bell shows time of acknowledgement | Shows time the fault was raised (only time on the record) |
| Dark theme | Still not chosen (open in STEP-LOG) |

## Still on the old look (not in the upload, so not redesigned)
SignIn, MachinesList, MachineDetail, Settings, Admin, DemoPanel, Tracker, LiveWindow. They work inside the new frame.

## Differences from ui-shell.md
- "Critical or abnormal" tile is now "Critical"; Warning tile counts warning + abnormal (same first level, open item O-10).
- Sign out is a button (calls the server), not a link to /signin.
