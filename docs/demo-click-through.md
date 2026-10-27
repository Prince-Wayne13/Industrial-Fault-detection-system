# Click-through: every screen, three roles

Start: `python app.py` in `system/backend`, `npm run dev` in `system/frontend`. Use three browser tabs; each tab is its own sign-in.
Accounts: `operator1`, `engineer1`, `admin1`. Password is `demo-password-for-` plus the username. "Demo accounts" on the sign-in page fills the form.
Tick each line. Write the page and what looked wrong beside any line that fails.

## 0. Sign in (any tab)
- [ ] Wrong password: red notice, no sign-in.
- [ ] Right password: lands on Overview inside the new frame (side nav, top bar).
- [ ] Tab title and the brand at top left both say Fault-Detect.

## 1. Operator (`operator1`)
- [ ] Side nav shows Overview, Machines, Settings, and Demonstration (Demo panel, Tracker). No Admin.
- [ ] Overview: five tiles add up (Total = machines shown). Cards grouped Motors, Water pumps, Backup power. Numbers move every second.
- [ ] Search "pump" then Enter: opens Pump 1. Search "zzz" then Enter: box turns red.
- [ ] Connection icons: Bluetooth glows (near range). Wi-Fi plain.
- [ ] Demo panel, "Sustained warning": countdown bottom left, then a pop-up bottom right with machine, "Temperature is too high", the reading and the limit.
- [ ] Pop-up stays until Acknowledge. After it: pop-up gone, bell shows 1, bell list shows the fault, choosing it opens Motor 1.
- [ ] Machines page: filter by Type and Status. Names open the machine page.
- [ ] Machine page: graph with Day, Week, Month, Year. Live window shows 10 slots. Operator cannot Resolve (button absent or refused).
- [ ] Settings: change sign-out time, change password (15 characters or more). Engineer limits not editable.
- [ ] Name panel: full name, role, Settings, Sign out. Sign out returns to sign-in.

## 2. Engineer (`engineer1`)
- [ ] Same side nav as Operator.
- [ ] Gets its own pop-up for the same fault, and acknowledges it separately (FR-8).
- [ ] Machine page: Resolve works; bell count drops by one. Start and end Maintenance; card shows the Maintenance tag.
- [ ] Settings: change a limit. Too-high value refused with a message. Valid value saves and shows in the change log.
- [ ] Demo panel, "Pump speed swings": after about 10 seconds a Pump 1 pop-up says "Speed is swinging up and down".
- [ ] Demo panel, "Lone spike": no pop-up.
- [ ] Demo panel, "Bad reading": Invalid tag beside the number. "Sensor goes silent": Sensor fault tag, no number.
- [ ] Machine page: CSV report downloads.

## 3. Administrator (`admin1`)
- [ ] Side nav shows Overview, Admin, Settings. No Machines.
- [ ] No pop-ups ever, even during "Two faults at once".
- [ ] Bell shows the storage alert only (when storage is above 75%), titled "Storage alert".
- [ ] Admin: storage bar, users list (add one), machines list (add and remove one), change log.
- [ ] Administrator cannot download a report or resolve a fault (refused).
- [ ] Try `/machines` by typing it: "Not allowed".

## 4. Connection and look
- [ ] Demo panel "Remote range": Wi-Fi icon glows, Bluetooth plain.
- [ ] "Cut connection": both icons grey with a slash and the word Offline; yellow notice on Overview; "Restore connection" clears it and the count of waiting windows goes to 0.
- [ ] Stop the back end: red notice "Live connection lost". Start it again: notice clears.
- [ ] Narrow the window under 900 px: side nav shrinks to icons, nothing overlaps.
- [ ] Press Escape with the bell open: it closes.
- [ ] Tab through the top bar with the keyboard: every control shows a visible focus ring.

## 5. End
- [ ] Demo panel "Reset everything". Tracker page loads and shows no row marked "not set" that should be built.
