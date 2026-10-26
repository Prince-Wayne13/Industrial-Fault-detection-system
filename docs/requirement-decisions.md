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
| PR-001 | The status of each machine updates at least every 10 seconds. This replaces the 60-second alert target. The 10-second check exists to rule out a random reading. | Team, 26 Oct 2026 |
| PR-001a | When the status is critical, the alert appears immediately after the status confirms it, and no later than 2 seconds after, allowing for delay. It does not alert on a single reading. | Team, 26 Oct 2026 |
| PR-001b | If an alert is shown more than 2 seconds after its status confirms the fault, the alert is still shown, the delay is written to the log, and the dashboard shows an "alerts delayed" notice. | Team, 26 Oct 2026 |
| PR-001 (reason) | Why the target is acceptable: a late alert means part of the system is interrupted or slow. The fault is still recorded and stays open, and is shown to the next user who connects. The cost of lateness is that the equipment runs longer before anyone acts. Answers examiner question 6 (why 60 seconds). | Team, 26 Oct 2026 |
| Section 5, Appendix D | PR-001 is tested by measuring the gap between the time the status confirms a fault and the time the pop-up appears, both on the synchronized clock (FR-25). | Accepted, 26 Oct 2026 |
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
| PR-005 | At least one reading per second per parameter per machine, so the load is machines × parameters per second. The minimum is 40 a second (10 machines × 4 parameters). A machine may have extra parameters, and the system shall still keep up. | Team, 24 Oct 2026 |
| PR-002 | The dashboard updates every 2 seconds. | Team |
| FR-9 | A normal 10-second window keeps only its status and time stamp. Its readings are deleted after a day. | Team |
| FR-9 | A warning or critical window keeps its readings together with its status. | Team |
| FR-9 | The status and the data it used are added to the database. | Team |
| NFR-10 | "At least 30 days" is replaced. Statuses and fault or warning bundles stay until the 75% storage alert. The system never deletes them by itself. | Team |
| PR-006 | Re-sized: at least one day of raw readings is 10 machines × 4 parameters × 86,400 seconds in a day (24 × 60 × 60) = 3,456,000, plus statuses and fault bundles. Extra parameters add 864,000 a day per 10 machines for each one. | Derived, 24 Oct 2026 |
| FR-12, FR-20, NFR-6 | Local storage runs at the same time as the main store, as an active backup. This makes the 1% loss limit realistic. | Team |
| FR-12, FR-20, NFR-6 | The same keep and delete rules apply to both stores. | Proposed |
| NEW (storage alert) | At 75% of storage used, an alert goes to the Administrator only. The Administrator manages storage. This is the Administrator's one alert. Replaces "all connected users, especially the Administrator". | Team, 24 Oct 2026 |
| Section 1.2 | What personnel do after the storage alert is out of scope. | Team |
| UC-3 | Reports list statuses and fault or warning bundles. They cannot show normal readings older than a day. | Derived |

### Roles and access

| Req | Decision | Source |
| --- | --- | --- |
| Section 2.3, 3.1.1, FR-27 | The Administrator manages the system (accounts, equipment, settings). They are not an operational user and do not acknowledge alerts. | Team |
| Section 2.3, 3.1.1 | There are three roles: Operator, Engineer, Administrator. The Management / Supervisor role is dropped. Answers examiner question 5. | Team, 24 Oct 2026 |
| Section 3.1.1, FR-7, FR-8 | Operator and Engineer see fault pop-ups and can acknowledge. The Administrator sees none. Reports: Operator and Engineer only. All three roles can view status, readings and fault history. | Team, 26 Oct 2026 |
| FR-17, FR-18, FR-23 | Only the Engineer can resolve a fault, use maintenance mode, and change limits. | Team, 26 Oct 2026 |
| Section 2.3 | The reason for three roles is written in one sentence: three different sets of rights (watch and acknowledge, fix and tune, manage the system). There is no "exactly one role" rule. The Operator is the first responder on shift. The Engineer diagnoses and fixes, often remotely. | Team, 26 Oct 2026 |
| Section 3.1.1, storage alert | Only the Administrator receives the storage alert and manages storage. | Team, 24 Oct 2026 |
| NEW (limits) | The Engineer can change the warning and critical limit per equipment type and parameter from the dashboard, with no restart or rebuild. A new limit is rejected if the warning limit is not below the critical limit. A change applies to readings received after it. Answers examiner question 2. | Accepted, 24 Oct 2026 |
| NEW (fault record) | Each fault record stores the limit in force when it was raised. | Accepted, 24 Oct 2026 |
| FR-23, FR-22 | The engineer may change limits, as long as every change is logged. | Team |

### Security (new requirements)

| Req | Decision | Source |
| --- | --- | --- |
| NEW (passwords) | At least 15 characters, with 64 or more allowed. No forced mix of capitals, numbers or symbols. No forced changes on a schedule. Common or leaked passwords refused. | Accepted |
| NEW (failed attempts) | After 5 wrong attempts, wait 15 minutes. Optional. | Accepted |
| FR-26 | Session timeout is 5 minutes by default and at most 5 minutes. Each user can shorten their own, down to a minimum of 1 minute. | Team, 24 Oct 2026 |
| NEW (data on the way) | Secure web connection (HTTPS, TLS 1.2 or newer). | Accepted |
| NEW (password storage) | Passwords stored scrambled so nobody can read them back. Suggestion in Appendix B. | Accepted |
| Appendix B | The security rules (password length, lockout, HTTPS, stored passwords, timeout) are written as requirements. The methods (hashing tool, TLS setup) are suggestions in Appendix B. The failed-attempt lockout uses "should". | Team, 24 Oct 2026 |
| PR-007 | Start-up time is 60 seconds from launch until monitoring is active. | Accepted |

### Demonstration and design

| Req | Decision | Source |
| --- | --- | --- |
| DC-006, Appendix B | The demonstration is a dashboard with simulated modes that inject faults. It stays in Appendix B and DC-006. | Team |
| DC-006, Section 5 | Question 7 settled the small way. The product is the real system. The demonstration is a dashboard with simulated data and a fault-injection mode. One sentence says so in DC-006 and Section 5. FR-11 and NFR-5 are not rewritten. | Team, 26 Oct 2026 |
| FR-5, Appendix A | Where the limits define only one abnormal level, the system classifies the condition as normal or abnormal. Pumps and backup power have one abnormal level, and motor vibration has no warning level. Closes examiner question 8. | Team, 26 Oct 2026 |

---

## C. Proposed, waiting for a decision

| Req | Proposal |
| --- | --- |
| FR-17, FR-18 | Replace "authorized user" with a named role. Operator and Management stay view-and-acknowledge and view-and-reports. |
| Sections 1.2, 2.2 | Add reports, maintenance mode, acknowledging and resolving faults, the trend check and administration. |
| Section 1.1 | One sentence: "shall" is required, "should" is a preference, requirements do not use "must". Then change "must" to "shall" where binding. |
| Section 4.4 | Each reading carries equipment identifier, parameter, value with unit, and time taken. Send method in Appendix B to be chosen. |
| PR-003 | State what happens beyond 10 pieces of equipment. |
| Section 5, Appendix D | Add acceptance rows for FR-6, FR-13, FR-14, FR-18, FR-19 and the new requirements. Add test methods for PR-003 to PR-007 and NFR-8 to NFR-10. |
| Appendix C | Add owner and date columns. |
| Diagrams | Accepted 26 Oct 2026, to be drawn once the wording is final: (1) context diagram, (2) use-case diagram, (3) diagram of what the system keeps, (4) processing flow from reading to alert including the sanity check, 10-second status check and local backup, (5) fault lifecycle (open, acknowledged, resolved) with maintenance mode and the late-alert notice. |
| Front matter | Version, date, authors, reviewer, revision history. Refresh the contents page. Define trend check, sensor fault, maintenance mode, acknowledge and resolved. |
| DC-006 to DC-008, Section 2.4, 2.5, 3.6 | Remove repeated text. Needs your consent. |
| TTD, TTA, MTBF, FLA | Use or remove these unused terms. Removal needs your consent. |
| Appendix C | Label or move the "Final Implementation Check Before Submission" list. Needs your consent. |

---

## D. Still open

| Item | Detail |
| --- | --- |
| Section 3.1 or 4 | Does the course handout put interface requirements in Section 3.1? |

The fuller list of open questions is in `open-items.md`. Design-level choices are in `design-decisions.md`.
