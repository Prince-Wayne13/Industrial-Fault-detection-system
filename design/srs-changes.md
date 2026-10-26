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
| 10 | Pages 4, 5 and 6 merged into other pages | [[UC-2]], [[UC-3]], [[UC-6]] | design only, no wording change |

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
- See [[03-machine-detail]].

### 5. Machines list and search (new requirement)

- **Suggested:** the system shows a list of all registered machines that can be filtered by type and by status. Choosing a machine opens its page. A search bar in the top bar finds a machine by name.
- Neither is in the SRS today, so both show as extra on the tracker.
- See [[11-machines-list]] and [[top-bar]].

### 6. Full name

- **Suggested addition to [[UC-5]]:** a user account holds a full name, a username, a role and a password. The name side bar shows the full name and the role.
- Confirmed by you.

### 7. The Settings page

- **Sign-out time:** no wording change to [[FR-26]]. Each person sets their own, from 1 to 5 minutes. It now sits in Settings.
- **Limits:** [[FR-23a]] says an Engineer changes limits "from the dashboard". **Suggested:** "from the Settings page".
- **Theme (new):** a person can switch the screen between light and dark. Not in the SRS, so it shows as extra.
- See [[07-settings]].

### 8. The clash in FR-27

- **Now:** [[FR-27]] limits configuration, user accounts and machine registration to the Administrator. [[FR-23a]] lets the Engineer change limits.
- **Suggested:** add to [[FR-27]]: "except the warning and critical limits, which an Engineer changes (FR-23a)".

### 9. The Administrator

- **Decided:** the Administrator cannot reset another person's password.
- **Decided:** the Administrator can see the Overview but gets no fault pop-ups and no fault bell list ([[FR-7b]]).
- **Suggested:** the role table says the Administrator may view the Overview. Nothing else about the role changes.
- See [[08-admin]] and [[02-overview]].

### 10. Merged pages

- Alerts, History and reports, and Maintenance are no longer separate pages. The fault pop-up, the bell list and the machine page do their jobs.
- No requirement changes. [[UC-2]], [[UC-3]] and [[UC-6]] keep their steps, and only the screens that carry them moved.

## Not decided yet

- Can a resolved fault be switched back to open? The SRS has no way to do it.
- Can the Administrator open a machine's page from an Overview card?
- Does a limit belong to a machine type or to each machine on its own? [[FR-23a]] reads as per type.
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
