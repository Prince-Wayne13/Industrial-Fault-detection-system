# Design Decisions

How the system will be built. These are **choices**, not requirements: a requirement says what the system must do, and a design decision says how we do it. The current design decisions are in Appendix B of the SRS. This file keeps them, plus the design-level choices made since, in one place where we can keep discussing them.

**Status:** Decided / Undecided.
**Source:** SRS Appendix B, or Team (you told me the team decided it).

| ID | Area | Decision | Status | Source | Affects |
| --- | --- | --- | --- | --- | --- |
| DD-01 | Equipment data | A Simulink model produces simulated sensor data in place of real sensors. | Decided | Appendix B | Section 4.2, DC-006 |
| DD-02 | Sending data | Simulated data reaches the processing part over a UDP or TCP connection. | **Undecided** | Appendix B | Section 4.4 |
| DD-03 | Web back end | Flask (Python). Replaces "Flask or FastAPI" and "PHP or Flask". | Decided | Team, 24 Oct 2026 | Appendix B, security suggestions |
| DD-04 | Storage | Appendix B says one SQLite database. See DD-10 for the local backup. | Decided, but see DD-10 | Appendix B | FR-9, FR-20, NFR-10 |
| DD-05 | Fault detection | Threshold screening first, then a logistic regression model classifies the condition. No model is trained yet. | Decided | Appendix B | FR-4, FR-5, NFR-1, NFR-2 |
| DD-06 | Processing flow | Incoming readings pass a sanity check first. Wrong-format readings are recorded and kept out. Clean readings go to the status model. The model collects 10 seconds of readings, then updates the status. The status and the data it used are added to the database. | Decided (not yet in the SRS) | Team | FR-6, FR-9, FR-14, UC-2 step 4, the flow note under FR-5 |
| DD-07 | Dashboard | The back end serves a web dashboard using a REST API and WebSocket updates. It works in the latest two major versions of Chrome, Firefox and Edge. The dashboard updates every 2 seconds. | Decided | Appendix B and Team | PR-002, NFR-8 |
| DD-08 | Connection modes | Near-range and remote-range are simulated, with a manual switch for the demonstration. | Decided | Appendix B | FR-11, DC-006 |
| DD-09 | Alert delivery | Alerts appear as pop-ups on the dashboard of connected users. Nothing is sent outside the software. The Administrator gets no fault alerts. | Decided (not yet in the SRS) | Team | FR-7, FR-8 |
| DD-10 | Backup | Local storage runs at the same time as the main store, as an active backup. The same keep and delete rules are assumed for both. | Decided (details open) | Team | FR-12, FR-20, NFR-6 |
| DD-11 | Clean-up | A normal 10-second window keeps only its status and time stamp, and its readings are deleted after a day. Warning and critical windows keep their readings. | Decided (not yet in the SRS) | Team | FR-9, NFR-10, PR-006 |
| DD-12 | Storage alert | An alert goes to the Administrator only when 75% of the set storage is used. What happens next is for site personnel. | Decided (not yet in the SRS) | Team | NEW storage alert, Section 1.2 |
| DD-13 | Dashboard values | The raw value of every reading shows on the dashboard, including wrong-format ones, which are marked invalid. | Decided (marking is my wording) | Team | FR-14 |
| DD-14 | Security suggestions | Secure web connection (HTTPS, TLS 1.2 or newer). Passwords stored scrambled with a salt. Wait 15 minutes after 5 wrong attempts. Session timeout 5 minutes by default, at most 5, shortened per user. These go in Appendix B as suggestions. | Decided | Team | NEW security requirements, FR-26 |

| DD-15 | Web front end | The dashboard is built in React using JSX. It talks to the Flask back end over the REST API and WebSocket updates in DD-07. | Decided | Team, 24 Oct 2026 | DD-07, Section 4.1, Appendix B |

## Questions to settle

- **DD-04 and DD-10:** what is the "main store" and what is the "local copy"? Is the main store online? DC-007 says the system must work without continuous internet. How do the two stay in step?
- **DD-06:** is the "status model" the same as the logistic regression classifier in DD-05? Does threshold screening still run on each reading?
- **DD-02:** UDP or TCP, and does the Simulink link need a special real-time toolbox? Appendix C already lists this as open.
