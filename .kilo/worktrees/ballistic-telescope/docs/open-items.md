# Open Items

Everything still waiting for a decision. When an item is settled, record it in `requirement-decisions.md` or `design-decisions.md`, then delete it from here.

| ID | Question | Related | Suggestion | Owner | Date |
| --- | --- | --- | --- | --- | --- |
| O-1 | What is the shortest session timeout a user may set? | FR-26 | 1 minute | | |
| O-2 | Is the 10-second alert target counted from the status update that confirms the fault? | PR-001 | Yes. Counting from the start of the fault leaves no time, because the window takes up to 10 seconds to fill. | | |
| O-3 | Final wording of NFR-6 now that local storage is an active backup. | NFR-6, FR-20 | Draft once DD-10 is clear. | | |
| O-4 | Does the course handout put interface requirements in Section 3.1? | Section 3.1, Section 4 | Check the handout or ask the lecturer. Leave Section 4 as it is meanwhile. | | |
| O-5 | Is the status model the same as the logistic regression classifier? Does threshold screening still run per reading? | DD-05, DD-06, FR-4, FR-5 | | | |
| O-6 | Which web stack: PHP, Flask or FastAPI? | DD-03 | | | |
| O-7 | What is the main store, and how do the main store and local copy stay in step? | DD-04, DD-10 | | | |
| O-8 | Why is the alert target acceptable? One sentence: what goes wrong if an alert is later. | PR-001 | The examiners asked for this. | | |
| O-9 | Does acknowledging leave the fault open until it is resolved? | FR-8, FR-17 | Yes. | | |
| O-10 | Which role may resolve a fault and use maintenance mode? Are Operator and Management roles kept as they are? | FR-17, FR-18, Section 3.1.1 | Technician and Administrator for maintenance mode. Operator and Management unchanged. | | |

The Owner and Date columns are empty on purpose. The examiners criticised open items with no owner or date.
