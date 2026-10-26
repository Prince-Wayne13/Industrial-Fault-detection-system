# Next Steps: How We Finish the SRS

Written 26 October 2026, after examiner questions 1 to 8 were settled. This is the approach we agreed in discussion. Read it with `v2-clear-statements.md` (the agreed wording) and `workflow.md` (the git steps).

## Group members

Prince Msowoya, Zilpah Kalipa, Theresa Somanje, Opra Chikwangwala, Steven Nkhoma, Akuzike Mphande, Timothy Kaperenganya.

## The guiding rule

**Keep it light and finish.** The team was overwhelmed by how much was being changed, so we stopped deep fixing. The lecturer wants to see a dashboard, a way to inject faults, and an SRS that leads to a design. Anything that does not serve that waits.

Each requirement is a clear statement: one subject, one action, one number or condition, and one test that can prove it. No vague words ("appropriate", "in time to act").

## What is settled (do not reopen)

- Questions 1 to 8 are settled. The wording is in `v2-clear-statements.md`. The reasons are in `requirement-decisions.md`.
- Three roles: Operator, Engineer, Administrator. The Operator is the first responder and acknowledges; the Engineer resolves, uses maintenance mode and changes limits; the Administrator manages the system and the storage alert. Reports: Operator and Engineer.
- Flask back end (DD-03). React with JSX front end (DD-15).
- Alert timing: status updates at least every 10 seconds; a critical alert shows within 2 seconds of the status confirming it; a late alert is still shown, logged, and flagged on the dashboard.
- The demonstration is a dashboard with simulated data and a fault-injection mode. FR-11 and NFR-5 are not rewritten.

## The order of work

1. **Apply the statements to the Word file** (`srs/SRS_Industrial_Fault_Detection.docx`) in one pass, topic by topic, following `workflow.md`: decide, apply, export, commit, tag. One topic per commit, and never mix a renumbering with a new requirement. Only one person edits the Word file at a time, because Word cannot merge two people's edits. Requirement numbers in `v2-clear-statements.md` are provisional; fix the final numbers here and update every cross-reference (Section 5, Appendix D).
2. **Fix the front page:** version 2.0, today's date and the seven group members as authors (done). No revision history, because the 1.x versions never reached the lecturer. Still to do: name a reviewer if one is wanted, and refresh the contents page, and Section 1.5 (it still says Section 5 covers other requirements).
3. **Add the one-sentence demonstration note** to DC-006 and Section 5.
4. **Run `./scripts/export-md.sh`** (needs pandoc) so the plain-text copy matches the Word file. Never edit the `.md` copy by hand.
5. **Diagrams.** Done: the context diagram (Figure 1, Section 2.1) and the use-case diagram (Figure 2, Section 3.2), in the lecturer's style and checked label by label against UC-1 to UC-6, the role table and Section 4. Optional, drawn last once the wording is final: what the system keeps, the processing flow from reading to alert, and the fault lifecycle with maintenance mode and the late-alert notice.
6. **Run the 20-question checklist** (`review/general-questions-checklist.md`) and fill in the "After" column.
7. **Tag** `v2.0` and hand in.

## Open items that remain

Each needs an owner and a date, because the examiners criticised items with neither. The leans below are my suggestions and have not been confirmed.

| ID | Question | Lean |
| --- | --- | --- |
| O-4 | Does the course handout put interface requirements in Section 3.1? | Check the handout or ask the lecturer. Leave Section 4 as it is until then. |
| O-5 | Is the status model the same as the logistic regression classifier? | Treat them as the same. Threshold screening runs on every reading, then the classifier sets the status for each 10-second window. |
| O-7 | What is the main store, and how does it stay in step with the local copy? | The main store is the server's SQLite database. The local copy records the same readings at the same time and replays after an interruption. |
| O-9 | Does acknowledging leave the fault open until resolved? | Yes. Written as provisional in FR-8c. |
| DD-02 | UDP or TCP for the Simulink link? | TCP, because the 1% loss limit is hard to defend over UDP. If the link cannot do it, record that in Appendix C. |

## Housekeeping

- A full copy of the project is committed under `.kilo/worktrees/ballistic-telescope/`. It looks accidental. Remove it only with the team's agreement.
- Two points to double-check with the lecturer if asked: the Operator can acknowledge but not resolve, and if no Engineer is connected the fault stays open until the next connection.
- Sizing assumes 4 parameters per machine as a minimum; machines may have extra parameters, so PR-005 and PR-006 are written as a minimum and grow with the parameter count.
