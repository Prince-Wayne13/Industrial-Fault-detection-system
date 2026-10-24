# Requirement Decisions: Industrial Fault Detection SRS

Status on 17 October 2026. Requirement numbers are those in document version 1.6.

**Source column**
- **Team**: you told me the team decided this.
- **Accepted**: I proposed it and you accepted it.
- **Proposed**: my draft. Not confirmed yet.
- **Derived**: follows from a team decision (arithmetic or consequence).

**Requirement column**
- A number such as FR-7 means the requirement already exists and will be changed.
- **NEW** means there is no number yet. A number is given when it is added to the document.

---

## A. Already in version 1.6

| Req | Decision | Source |
| --- | --- | --- |
| FR-1 to FR-28 | Requirements count up in the order they appear. The access-control rules are FR-27 and FR-28. | Team |
| FR-6 | A single abnormal reading is never a fault. A check across recent readings comes first. The number is a placeholder [N] in v1.6. | Team |
| FR-13, FR-14 | Sensor-fault flag and invalid-reading rejection, moved from the non-functional list. | Team |
| FR-15 to FR-26 | Fault handling, maintenance mode, storage and recovery, admin log, limit-change history, multiple units, time source, session expiry. | Team |
| DC-001 to DC-008 | Design constraints (dust, humidity, heat, electrical noise, no named site, no hardware, no internet, course time). | Team |
| PR-001 to PR-007 | Performance requirements split out from the non-functional list. PR-007 start-up time is a placeholder. | Team |
| NFR-1, NFR-2, NFR-5 to NFR-10 | All non-functional requirements together in Section 3.5. | Team |
| NFR-6 | Short rule first, one-sentence explanation below it. | Team |
| NFR-8 | Everything visible on one laptop screen. | Team |
| PR-001 | Clock starts when the trend check confirms the fault. | Proposed, now replaced by section B |
| PR-002 | Dashboard shows a reading within 2 seconds. Does not include the trend check. | Proposed |
| FR-11 | Extra sentence saying both connection modes are simulated. | Proposed, to be removed |
| Section 4.1, 4.4 | Login, administrator functions, reports and shared time source added to the interfaces. | Proposed |
| Section 3.6, Section 5 | Other requirements moved into 3.6. Section 5 is now Acceptance Criteria. F1-score wording simplified in the table. | Team |

---

## B. Decided, not yet in the document

### Alerts and fault handling

| Req | Decision | Source |
| --- | --- | --- |
| FR-6 | The trend check is the status model collecting 10 seconds of readings, then updating the status. So [N] is a 10-second window. | Team |
| PR-001 | The alert target becomes 10 seconds, replacing 60. | Team |
| PR-001 | The 10 seconds is counted from the status update that confirms the fault. | Proposed, please confirm |
| FR-7 | Alerts appear as pop-ups to connected users with an operational role (near-range or remote). If nobody is connected, nobody is told. The fault stays open and shows at the next connection. | Team |
| FR-7 | The Administrator gets no fault alerts or pop-ups. | Team |
| FR-8 | Acknowledging writes a log record of which user did it, and when. | Team |
| FR-8, FR-17 | Acknowledging does not close the fault. It stays open until resolved. | Proposed |
| FR-14 | A sanity check runs first. Wrong-format readings are recorded and kept out of the status model. Clean readings go through. | Team |
| FR-14 | The raw value of a wrong-format reading still shows on the dashboard, marked as invalid. | Team (showing), Proposed (marking) |

### Data, sampling and storage

| Req | Decision | Source |
| --- | --- | --- |
| NEW (sampling) | One reading per second for every parameter on every machine. | Team |
| FR-13 | "Normal reporting interval" means 1 second. | Derived |
| PR-005 | At least one reading per second per parameter per machine. This is 30 a second for 10 machines with 3 parameters each. | Derived |
| PR-002 | The dashboard updates every 2 seconds. | Team |
| FR-9 | A normal 10-second window keeps only its status and time stamp. Its readings are deleted after a day. | Team |
| FR-9 | A warning or critical window keeps its readings together with its status. | Team |
| FR-9 | The status and the data it used are added to the database. | Team |
| NFR-10 | "At least 30 days" is replaced. Statuses and fault or warning bundles stay until the 75% storage alert. The system never deletes them by itself. | Team |
| PR-006 | Re-sized: one day of raw readings is 10 x 3 x 86,400 = 2,592,000, plus statuses and fault bundles. | Derived |
| FR-12, FR-20, NFR-6 | Local storage runs at the same time as the main store, as an active backup. This makes the 1% loss limit realistic. | Team |
| FR-12, FR-20, NFR-6 | The same keep and delete rules apply to both stores. | Proposed |
| NEW (storage alert) | At 75% of storage used, an alert goes to all connected users, especially the Administrator. This is the Administrator's one alert. | Team |
| Section 1.2 | What personnel do after the storage alert is out of scope. | Team |
| UC-3 | Reports list statuses and fault or warning bundles. They cannot show normal readings older than a day. | Derived |

### Roles and access

| Req | Decision | Source |
| --- | --- | --- |
| Section 2.3, 3.1.1, FR-27 | The Administrator manages the system (accounts, equipment, settings). They are not an operational user and do not acknowledge alerts. | Team |
| FR-23, FR-22 | The engineer may change limits, as long as every change is logged. | Team |

### Security (new requirements)

| Req | Decision | Source |
| --- | --- | --- |
| NEW (passwords) | At least 15 characters, with 64 or more allowed. No forced mix of capitals, numbers or symbols. No forced changes on a schedule. Common or leaked passwords refused. | Accepted |
| NEW (failed attempts) | After 5 wrong attempts, wait 15 minutes. Optional. | Accepted |
| FR-26 | Session timeout is 5 minutes by default and at most 5 minutes. Each user can shorten their own. | Team |
| NEW (data on the way) | Secure web connection (HTTPS, TLS 1.2 or newer). | Accepted |
| NEW (password storage) | Passwords stored scrambled so nobody can read them back. Suggestion in Appendix B. | Accepted |
| Appendix B | Security suggestions are listed there, not in the requirements. | Team |
| PR-007 | Start-up time is 60 seconds from launch until monitoring is active. | Accepted |

### Demonstration and design

| Req | Decision | Source |
| --- | --- | --- |
| DC-006, Appendix B | The demonstration is a dashboard with simulated modes that inject faults. It stays in Appendix B and DC-006. | Team |
| Appendix B | PHP or Flask is undecided. | Team |

---

## C. Proposed, waiting for a decision

| Req | Proposal |
| --- | --- |
| NEW (limits) | An authorised user can change limits per equipment type and parameter. Entered values are checked, for example that a warning limit is below the critical limit. |
| NEW (fault record) | Each fault record stores the limit in force when it was raised. |
| FR-17, FR-18 | Replace "authorized user" with a named role. Operator and Management stay view-and-acknowledge and view-and-reports. |
| FR-5, Appendix A | Classify as warning or critical where limits define those levels. Otherwise normal or abnormal. Pumps and backup power have one abnormal level, and motor vibration has no warning level. |
| NFR-5 | Rewrite as real availability: 95% of the time in a period [to be agreed], not counting announced restarts. |
| FR-11 | Remove the demonstration sentence and the added simulation note. Needs your consent. |
| Sections 1.2, 2.2 | Add reports, maintenance mode, acknowledging and resolving faults, the trend check and administration. |
| Section 1.1 | One sentence: "shall" is required, "should" is a preference, requirements do not use "must". Then change "must" to "shall" where binding. |
| Section 4.4 | Each reading carries equipment identifier, parameter, value with unit, and time taken. Send method in Appendix B to be chosen. |
| PR-003 | State what happens beyond 10 pieces of equipment. |
| Section 5, Appendix D | Add acceptance rows for FR-6, FR-13, FR-14, FR-18, FR-19 and the new requirements. Add test methods for PR-003 to PR-007 and NFR-8 to NFR-10. |
| Appendix C | Add owner and date columns. |
| Diagrams | Context diagram, use-case diagram, and a diagram of what the system keeps. |
| Front matter | Version, date, authors, reviewer, revision history. Refresh the contents page. Define trend check, sensor fault, maintenance mode, acknowledge and resolved. |
| DC-006 to DC-008, Section 2.4, 2.5, 3.6 | Remove repeated text. Needs your consent. |
| TTD, TTA, MTBF, FLA | Use or remove these unused terms. Removal needs your consent. |
| Appendix C | Label or move the "Final Implementation Check Before Submission" list. Needs your consent. |

---

## D. Still open

| Item | Detail |
| --- | --- |
| FR-26 | Shortest timeout a user may set. I suggest 1 minute. |
| PR-001 | Confirm the 10 seconds is counted from the status update that confirms the fault. |
| NFR-6 | Final wording now that local storage is an active backup. |
| Section 3.1 or 4 | Does the course handout put interface requirements in Section 3.1? |

The fuller list of open questions is in `open-items.md`. Design-level choices are in `design-decisions.md`.
