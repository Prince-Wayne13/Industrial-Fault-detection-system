# Open Items

Everything still waiting for a decision. When an item is settled, record it in `requirement-decisions.md` or `design-decisions.md`, then delete it from here.

| ID | Question | Related | Suggestion | Owner | Date |
| --- | --- | --- | --- | --- | --- |
| O-4 | Does the course handout put interface requirements in Section 3.1? | Section 3.1, Section 4 | Check the handout or ask the lecturer. Leave Section 4 as it is meanwhile. | | |
| O-5 | Is the status model the same as the logistic regression classifier? Does threshold screening still run per reading? | DD-05, DD-06, FR-4, FR-5 | | | |
| O-7 | What is the main store, and how do the main store and local copy stay in step? | DD-04, DD-10 | | | |
| O-9 | Does acknowledging leave the fault open until it is resolved? | FR-8, FR-17 | Yes. | | |
| O-10 | "Warning" and "abnormal" are the same first level. Use one word everywhere? | FR-5, srs-changes | Proposed wording for FR-5: "A parameter with two limits has the statuses normal, warning and critical. A parameter with one limit has normal and abnormal. 'Warning' and 'abnormal' are the first level." The dashboard shows the word each parameter really has. The Overview tile counts both under "Warning". Words live in `frontend/src/status.js`, so a change is one edit. | | |
| O-11 | The SRS gives no most number of machines, only at least 10 (PR-003). Is that enough? | PR-003, FR-24 | No cap in the code. Proposed wording for PR-003: "The system supports at least 10 machines. It was run with 11 in the heavy-load demonstration. No upper limit is set." | | |

The Owner and Date columns are empty on purpose. The examiners criticised open items with no owner or date.
