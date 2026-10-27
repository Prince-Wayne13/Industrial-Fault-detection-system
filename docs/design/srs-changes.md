---
title: Changes the design asks of the SRS
status: draft
srs-version: v2.0
tags: [design, srs-changes]
---

# Changes the design asks of the SRS

Back to [[page-map]].

Every decision made while designing that is not in SRS v2.0, gathered in one place. When the design is finished, the SRS is edited from this list. The wording below is a suggestion for each edit. Nothing has been changed in the SRS yet.

## Summary

| # | Change | Requirements touched | Kind |
| --- | --- | --- | --- |
| 1 | Each person acknowledges a fault for themselves | [[FR-7]], [[FR-8]], [[FR-8a]], [[FR-8b]], [[FR-17]] | changes a rule |
| 2 | The fault pop-up stays until acknowledged | [[FR-7]], [[FR-7a]] | adds detail |
| 3 | A bell list of acknowledged, unresolved faults | new, after [[FR-8b]] | new |
| 4 | Day, Week, Month, Year graphs and report on the machine page | [[FR-10]], [[UC-3]] | adds detail |
| 5 | A machines list with a filter, and a search bar | new, after [[FR-24]] | new |
| 6 | Accounts hold a full name, shown with the role | [[UC-5]], [[FR-27]] | adds detail |
| 7 | A Settings page: theme, sign-out time and limits | [[FR-23a]], [[FR-26]], new | adds detail and new |
| 8 | Limits are the exception to Administrator-only configuration | [[FR-27]], [[FR-23a]] | fixes a clash |
| 9 | The Administrator cannot reset passwords, and can see the Overview | [[UC-5]], role table | adds detail |
| 10 | Alerts, History and reports, and Maintenance merged into other pages | [[UC-2]], [[UC-3]], [[UC-6]] | design only, no wording change |
| 11 | There are two stores: an online database and a local store, written at the same time. Appendix B (DD-04, DD-10) says one SQLite database. | Appendix B, [[FR-12]], [[NFR-6]] | no |
| 12 | The log also records acknowledgements and resolved faults, is saved in the database and is for the Administrator only | [[FR-22]], [[FR-23]], [[FR-8a]] | changes a rule |
| 13 | Every parameter can have all four limits, and any limit can be left out | [[FR-4]], [[FR-5]], [[FR-23a]], [[FR-23b]] | changes a rule |
| 14 | Fault pop-ups show one at a time | [[FR-7]], [[FR-7a]] | adds detail |
| 15 | A window is flagged by the model's fault score, not by all 10 readings | [[FR-6]], Appendix B | adds detail |
| 16 | Passwords are at least 8 characters | [[FR-28a]] | already applied in the SRS |
| 12 | "Set storage" means the set size of the local storage file. The 75% alert and the full-store case use it. | [[FR-21a]], [[NFR-10]], [[PR-006]] | no |

## The detail

### 1. Each person acknowledges for themselves

- **Now:** any Operator or Engineer can acknowledge a fault from its alert ([[FR-8]]).
- **Suggested:** each connected Operator and Engineer acknowledges a fault for themselves from their own alert. One person acknowledging does not count for another. An Engineer has to have acknowledged a fault before marking it resolved ([[FR-17]]).
- **Unchanged:** the system records who acknowledged and when ([[FR-8a]]). Acknowledging does not close the fault ([[FR-8b]]).

### 2. The pop-up stays

- **Suggested addition to [[FR-7]]:** the pop-up stays on a person's screen until that person acknowledges it.
- See [[fault-popup]].

### 3. The bell list (new requirement)

- **Suggested:** the system shows each Operator and Engineer a count of the faults they acknowledged that are not yet resolved. They can open a list of those faults, and choosing one opens that machine's page. The count goes down when an Engineer resolves a fault.
- The Administrator's bell carries the storage alert only ([[FR-21a]]).
- See [[top-bar]].

### 4. Graph and report on the machine page

- **Now:** reports are for a chosen machine and date range ([[FR-10]], [[UC-3]]).
- **Suggested:** the machine page offers a graph and a report for a day, a week, a month or a year.
- **Limit to state in the SRS:** the readings of a normal period are deleted after 24 hours ([[FR-9b]]). Longer periods show status over time, with full readings only around warnings and faults.
- See [[machine-detail]].

### 5. Machines list and search (new requirement)

- **Suggested:** the system shows a list of all registered machines that can be filtered by type and by status. Choosing a machine opens its page. A search bar in the top bar finds a machine by name.
- Neither is in the SRS today, so both show as extra on the tracker.
- See [[machines-list]] and [[top-bar]].

### 6. Full name

- **Suggested addition to [[UC-5]]:** a user account holds a full name, a username, a role and a password. The name side bar shows the full name and the role.
- Confirmed by you.

### 7. The Settings page

- **Sign-out time:** no wording change to [[FR-26]]. Each person sets their own, from 1 to 5 minutes. It now sits in Settings.
- **Limits:** [[FR-23a]] says an Engineer changes limits "from the dashboard". **Suggested:** "from the Settings page".
- **Theme (new):** a person can switch the screen between light and dark. Not in the SRS, so it shows as extra.
- See [[settings]].

### 8. The clash in FR-27

- **Now:** [[FR-27]] limits configuration, user accounts and machine registration to the Administrator. [[FR-23a]] lets the Engineer change limits.
- **Suggested:** add to [[FR-27]]: "except the warning and critical limits, which an Engineer changes (FR-23a)".

### 9. The Administrator

- **Decided:** the Administrator cannot reset another person's password.
- **Decided:** the Administrator can see the Overview but gets no fault pop-ups and no fault bell list ([[FR-7b]]).
- **Suggested:** the role table says the Administrator may view the Overview. Nothing else about the role changes.
- See [[admin]] and [[overview]].

### 10. Merged pages

- Alerts, History and reports, and Maintenance are no longer separate pages. The fault pop-up, the bell list and the machine page do their jobs.
- No requirement changes. [[UC-2]], [[UC-3]] and [[UC-6]] keep their steps, and only the screens that carry them moved.

### 11 and 12. The stores

- **Now:** Appendix B says the system uses one SQLite database, with a local backup in DD-10.
- **Suggested:** the system writes to an online database and to a local store at the same time. The local store has a set size, and "set storage" in [[FR-21a]] means that size. When the local store is full, saving fails and the system keeps the new readings in temporary storage ([[FR-20]]).
- See [[engine]] and [[build-plan]].

### 12. The activity log

- **Now:** [[FR-22]] logs administrative actions: user account changes, equipment registration, threshold or configuration changes. [[FR-23]] keeps the previous value of a limit and the date of change.
- **Built and suggested for [[FR-22]]:** the log also records each acknowledgement (who, which fault, when) and each resolved fault. The log is saved in the local and the online database, so it survives a restart. Only the Administrator can read it.
- **The clash:** [[FR-23]] keeps the old limit and its date, and the log is where they live, but an Engineer who changes a limit cannot read the log. **Suggested:** say in [[FR-23]] that the previous value and date are kept in the log, which the Administrator reads. If the Engineer must see earlier values, the Settings page has to show them. Your decision.
- See [[logs]] and [[settings]].

### 13. Limits: all four, and any can be left out

- **Now:** [[FR-23a]] lets an Engineer change "the warning limit and the critical limit". Appendix A gives some parameters one limit only (for example motor speed has "below" only, pump temperature "above" only).
- **Built:** every parameter shows four limits: warning above, critical above, abnormal above and abnormal below. An Engineer can fill in any of them, change them or empty them. An empty limit is "not necessary" and is not used; only limits with a value count in the status. At least one limit must stay. Limits belong to each machine, not to a machine type.
- **Suggested wording for [[FR-23a]]:** "An Engineer shall be able to set, change or remove any limit of any parameter of a machine (warning, critical, abnormal above, abnormal below) from the Settings page, without restarting or rebuilding the system. A parameter shall keep at least one limit."
- **Suggested addition to [[FR-23b]]:** the system also rejects a change where "abnormal below" is not lower than the limits for too high.
- **Suggested addition to [[FR-5]]:** a parameter with no warning or critical limit uses normal or abnormal only (this already follows the sentence added to [[FR-5]] in version 2).
- See [[settings]].

### 14. Pop-ups one at a time

- **Suggested addition to [[FR-7]]:** when several faults are waiting, the screen shows one pop-up at a time, the most serious first (critical before warning, then the oldest). A small note says how many are waiting. When the person acknowledges one, the next appears.
- Every fault still reaches every connected Operator and Engineer, and each stays until that person acknowledges it ([[FR-7a]], change 2).
- See [[fault-popup]].

### 15. How a window is flagged

- **Now:** [[FR-6]] says an abnormal condition must "hold across the readings of the latest 10-second window". It does not say how much of the window. The design first used "all 10 readings". One dipped reading then hid a real fault, so a window of 9 critical readings and one normal one was called normal.
- **Built:** the trained model turns each window into a fault score (0 to 100%). At 50% or more the window is flagged, and critical needs its own score of 50% or more. In practice a window with 6 or more of 10 readings over a limit is flagged, and 5 or fewer is not. One spike alone never is. The training windows are labelled with a 60% share, kept in `TREND_FRACTION`.
- **Suggested addition to Appendix B** (the line about the model): "The model gives each 10-second window a fault score. A window is flagged when the score is at least 50%."
- **Gap, not built yet:** a window with fewer than 10 readings (after maintenance, a reconnect, or lost readings) is scored on what arrived, so 1 to 3 readings over a limit can flag it. [[FR-6]] says a single abnormal reading never makes a fault. Suggested guard: only flag a window that has at least 8 clean readings. See [[engine]].

### 16. Password length

- [[FR-28a]] now says "at least 8 characters" (was 15) in the SRS, the design notes, the back end and the screens. The lockout of 15 minutes ([[FR-28d]]) is a different number and did not change.

## Not decided yet

- Can a resolved fault be switched back to open? The SRS has no way to do it.
- Can the Administrator open a machine's page from an Overview card?
- Colours for the dark theme (see the end of this note).

## Colour palette

The colours for Fault-Detect. The same code is in `palette.css`, ready to use when the screens are built.

```css
/* Canvas & surfaces - diary/paper feel */
  --bg-canvas:      #dbdee0;
  --bg-card:        #F8F9FB;
  --bg-sidebar:     #2B3A4A;
  --bg-sidebar-hover: #344657;
  --bg-chart:       #F1F4F8;

  /* Brand colors - muted yacht blue palette + Gold */
  --primary:        #2C3A4C; /* Slightly darker, richer yacht blue */
  --primary-dim:    rgba(44, 58, 76, 0.08);
  --secondary:      #5B7C99;
  --secondary-dim:  rgba(91, 124, 153, 0.08);
  --gold:           #C4A35A; /* Premium gold accent */
  --gold-dim:       rgba(196, 163, 90, 0.1);
  --warning:        #B8A06A;
  --warning-dim:    rgba(184, 160, 106, 0.1);
  --teal:           #6B8E7B;
  --teal-dim:       rgba(107, 142, 123, 0.08);
  --red:            #A06B6B;
  --red-dim:        rgba(160, 107, 107, 0.1);
  --purple:         #7B6B8E;
  --purple-dim:     rgba(123, 107, 142, 0.1);

  /* Text hierarchy - soft, readable */
  --text-head:      #2D3748;
  --text-body:      #4A5568;
  --text-muted:     #8B9BB0;

  /* Borders - subtle paper edges */
  --border-faint:   #E5E8ED;
  --border-light:   #D5DAE1;
```

### How the colours could be used (a suggestion)

| Where | Colour |
| --- | --- |
| Page background | `--bg-canvas` |
| Machine cards and panels | `--bg-card` |
| Name side bar | `--bg-sidebar`, with `--bg-sidebar-hover` on hover |
| Graph background | `--bg-chart` |
| Normal status | `--teal` |
| Warning status | `--warning` |
| Critical status | `--red` |
| Maintenance mark | `--purple` |
| Accent, bell count, buttons | `--gold` |
| Headings, body text, small print | `--text-head`, `--text-body`, `--text-muted` |
| Lines and card edges | `--border-faint`, `--border-light` |

Status is always shown as a word as well as a colour, so the colour never carries the meaning alone.

### Open

- These colours are a light theme. Settings offers a dark theme too, and no dark colours are chosen yet.
