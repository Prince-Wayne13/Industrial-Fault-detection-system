# Industrial Fault Detection System: Requirements (SRS)

The requirements document for a system that watches motors, water pumps and backup power supplies, using simulated sensor data, and raises alerts when something goes wrong. A group course project (BEEE). The document goes to a client and a lecturer.

**Current version:** v1.6. The next version, v1.7, will apply the decisions listed in `docs/requirement-decisions.md` (part B).

## Group members

Prince Msowoya, Zilpah Kalipa, Theresa Somanje, Opra Chikwangwala, Steven Nkhoma, Akuzike Mphande, Timothy Kaperenganya.

## What is where

| Path | What it holds |
| --- | --- |
| `srs/SRS_Industrial_Fault_Detection.docx` | **The document.** Always the latest version. Edit this one. |
| `srs/SRS_Industrial_Fault_Detection.md` | A plain-text copy of the document, made by a script. Lets git show what changed between versions. Do not edit by hand. |
| `docs/requirement-decisions.md` | Every requirement decision, marked against its requirement number and who made it. |
| `docs/design-decisions.md` | How the system will be built, and the questions still open on that. |
| `docs/open-items.md` | Everything waiting for a decision, with space for an owner and a date. |
| `docs/glossary.md` | Plain meanings of the terms we use. |
| `docs/workflow.md` | How we work in this repo, step by step. |
| `docs/next-steps.md` | How we finish the SRS: the order of work, what is settled, what is left. |
| `docs/v1.7-clear-statements.md` | The agreed wording for examiner questions 1 to 8, ready to go into the Word file. |
| `docs/review/` | The examiner questions, our eight, and a 20-question checklist to run before every hand-in. |
| `docs/history/` | The team's two earlier drafts of the extra requirements. |
| `docs/plans/` | The plan for the v1.4 changes. |
| `scripts/export-md.sh` | Makes the plain-text copy from the Word file. |
| `CHANGELOG.md` | What changed in each version. |

Older versions are not kept as separate files. Git keeps them. See the tags `v1.3` to `v1.6`.

## Requirement numbers

| Prefix | Meaning | Section |
| --- | --- | --- |
| FR | Functional requirement: what the system does | 3.1 |
| UC | Use case: a user's goal, step by step | 3.2 |
| PR | Performance requirement: speed and capacity | 3.3 |
| DC | Design constraint: real-world limits | 3.4 |
| NFR | Other qualities: accuracy, reliability, usability, upkeep, data retention | 3.5 |
| AC | Acceptance criterion: how we check it | Section 5 |

## Known problems in v1.6

- The cover still says version 1.1, dated 20-09-2026, with no revision history.
- The contents page misses seven headings added in v1.4.
- Section 1.5 still says Section 5 covers other requirements. Section 5 is now Acceptance Criteria.
- The decisions in part B of the requirement register are not in the document yet.

The full list of findings is in `docs/review/general-questions-checklist.md`.

## Putting this on GitHub

1. Create a new **private** repository on GitHub. Leave it empty: no README, no licence.
2. In this folder, run:
   ```
   git remote add origin <the address GitHub shows you>
   git push -u origin main --tags
   ```
3. History is committed under the name "Claude". To use your own name, run `git config user.name "Your Name"` and `git config user.email "you@example.com"` before your next commit. Old commits keep the old name.

## Where to start

Read `docs/next-steps.md`, then `docs/open-items.md` and `docs/workflow.md`.
