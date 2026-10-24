# Examiner questions about our document

The eight questions in `source-questions/industrial-fault-detection_ours.pdf`, what each means, and where the answer is recorded.

The examiners use version 1.3 numbers. Today's numbers (v1.6): alert FR-6 is now **FR-7**; acknowledge FR-7 is now **FR-8**; connection modes FR-10 is now **FR-11**; administrator settings FR-12 is now **FR-27**; login FR-13 is now **FR-28**; the 60-second target NFR-3 is now **PR-001**; the 2-second target NFR-4 is now **PR-002**.

| # | Question in plain words | Status at v1.6 | Where the answer is recorded |
| --- | --- | --- | --- |
| 1 | How is anyone told of an alert, and what does acknowledging do? | Decided | FR-7, FR-8 in `../requirement-decisions.md` (B) |
| 2 | Can a limit change without rebuilding the system? | Decided that the engineer can change limits with every change logged. Requirement wording proposed. | FR-22, FR-23, NEW (limits) (B and C) |
| 3 | Which security requirements are missing, and who acknowledged a critical fault? | Decided | NEW passwords, FR-26, NEW secure connection (B) |
| 4 | How often is a reading taken, and what does that mean for storage and the 1% loss? | Decided | NEW sampling, FR-9, FR-13, PR-005, PR-006, NFR-6 (B) |
| 5 | Why four roles when the system tells two apart? | Partly decided. Administrator and engineer settled. Operator and Management assumed. | Section 2.3, 3.1.1, FR-27 (B and C) |
| 6 | Section layout, no diagrams, why 60 seconds? | PR-001 is now 10 seconds (counting point to confirm). Diagrams proposed. Layout waits for the handout. | PR-001 (B), `../open-items.md` |
| 7 | Which requirements are the product and which are the demonstration? | Demonstration settled. NFR-5 rewrite proposed. | DC-006, NFR-5, FR-11 (B and C) |
| 8 | Sourcing the numbers (question text cut off) | Mostly covered. One gap proposed. | FR-5, Appendix A (C) |
