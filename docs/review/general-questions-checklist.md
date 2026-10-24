# General questions checklist

Twenty questions drawn from all five examiner question sets. Run our document against them before every hand-in.

- **Result at v1.6** was checked on 17 October 2026.
- **After** is for you to fill in when you re-check.

| # | Question | Result at v1.6 | What was found | After |
| --- | --- | --- | --- | --- |
| 1 | Does the scope (Sections 1.2, 2.2) mention every function the detailed requirements contain, and nothing more? | Partly | Reports, maintenance mode, acknowledging and resolving, the trend check and administration are missing from 1.2 and 2.2. | |
| 2 | Do any two parts say different or opposite things? | No | Role table against Section 2.3. NFR-6 "retain all" against "lose no more than 1%". Section 1.5 against Section 5. Cover version. FR-5 against the pump and backup power limits. | |
| 3 | Is each thing said in only one place? | Partly | DC-006 to DC-008 repeat Section 2.4. The last bullet of 2.5 repeats FR-12. Section 3.6 repeats NFR-10. | |
| 4 | Are the assumptions really assumptions? | Partly | The last bullet of 2.5 is a promise. The fourth bullet mixes a dependency with a promise. | |
| 5 | Is every target one number with a way of measuring it, and free of vague words? | Partly | Open numbers: FR-6, PR-007, session timeout, "normal reporting interval". "Responsible personnel", "in time to act" and "appropriate" are vague. | |
| 6 | Do shall, should and must each mean one thing? | Yes, one gap | Requirements use "shall". "Must" appears in 1.1, 2.4, 3.3 and Appendix C. Nothing says what each word means. | |
| 7 | Are the numbers needed to size and test the system given? | No | No sampling rate, no interruption length, no timeout length. | |
| 8 | Can every requirement be traced to a check? | Partly | Nothing covers FR-6, FR-8, FR-10, FR-13 to FR-26, NFR-8 to NFR-10, PR-003 to PR-007. | |
| 9 | What happens when something fails or nobody is looking? | Partly | Failures are covered. Telling a person who is not watching was not. | |
| 10 | Can limits change without rebuilding, with every change recorded? | Partly | Changes are logged. No requirement makes limits adjustable. | |
| 11 | Is security specific? | Partly | Login, timeout and admin log exist. Protection of data, password rules, record of who acknowledged were missing. | |
| 12 | Do the roles make sense? | No | Three roles had identical rights. Section 2.3 contradicted the table. | |
| 13 | How long is data kept, what happens after, is there a backup? | Partly | "At least 30 days" with nothing after. No backup requirement. | |
| 14 | What breaks if the system grows tenfold? | Partly | PR-003 gives a minimum of 10. Nothing beyond. | |
| 15 | Is the product kept apart from the demonstration, and do open items have owners and dates? | Partly | NFR-5, FR-11 and Appendix C mix in coursework. Open items have no owner or date. | |
| 16 | Are there diagrams that match the text? | No | None. | |
| 17 | Are interfaces fully described and in the right place? | Partly | Section 4 is thin. UDP or TCP undecided. Placement against the handout unconfirmed. | |
| 18 | Is there document control and a correct contents page? | No | Cover says Version 1.1. No revision history. Contents page misses seven headings. Section 1.5 is wrong. TTD, TTA, MTBF and FLA are never used. | |
| 19 | Are numbers sourced, with the team's own choices marked? | Yes | Section 1.4, Appendix A and Appendix C. | |
| 20 | Is personal data protected and within the law? | Partly | User accounts and the admin log are held. Nothing says how they are protected or kept. | |
