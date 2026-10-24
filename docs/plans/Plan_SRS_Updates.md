# Plan: Everything Found and What Will Be Done

This lists every item found across the main document's handwritten notes and the two
supporting files, what each one means in plain terms, and exactly what will be done
about it in the updated main document. Nothing gets dropped without asking first.

---

## PART 1 — Items from the two supporting files

### A. Two items moved from the wrong list into the requirements list
The document currently has two items (called NFR-6a and NFR-7a) sitting in a list
meant for "how fast/reliable" qualities. But these two actually describe things the
system *does*, so they belong in the main requirements list instead.
- **Action:** Move them out, renumber as FR-14 and FR-15, keep the wording as-is.

### B. Fourteen brand-new requirements to add to the requirements list (FR-16 to FR-27)
Covering, in plain terms:
- Raising a separate warning for each thing going wrong at once, instead of lumping
  them together (FR-16)
- Not spamming repeat warnings for a problem that's already been flagged and is still
  waiting on someone (FR-17)
- Giving every fault a simple lifecycle: opened → someone's looked at it → fixed (FR-18)
- Letting an authorized person put a piece of equipment into "maintenance mode" for a
  set time, so it doesn't falsely alarm while someone is working on it (FR-19)
- Flagging on screen if maintenance mode has overrun its stated time (FR-20)
- If the main storage becomes full or unreachable, saving new readings somewhere
  temporary instead of crashing or silently losing them (FR-21)
- After a restart or crash, picking monitoring back up using the last known setup,
  rather than treating equipment as "unknown" (FR-22)
- Keeping a log of who changed user accounts, equipment, or settings, and when (FR-23)
- If a warning/danger threshold is changed, keeping the old value and the date it
  changed, instead of overwriting it silently (FR-24)
- Supporting more than one of the same kind of equipment (e.g. several motors) as
  separate, individually trackable units (FR-25)
- Keeping all parts of the system on the same clock, so timestamps line up (FR-26)
- Logging a user out after a period of inactivity, requiring them to log back in (FR-27)

**Action:** Add all fourteen as FR-16 through FR-27, worded as given.

### C. A Design Constraints list to fill the currently-empty section
Right now the section meant to list real-world limits on the design just points
elsewhere and says nothing itself. Eight items (DC-001 to DC-008) describe conditions
the equipment actually sits in and existing project limits, in plain terms:
- Dusty environments (sugar, flour, grain dust) affecting sensor accuracy (DC-001)
- Humid environments and occasional water exposure, e.g. breweries (DC-002)
- Heat up to 40°C on site, no assumption of an air-conditioned room (DC-003)
- Electrical noise/interference from nearby heavy machinery (DC-004)
- Not being built around one specific named factory, since not every industry's exact
  sensor numbers could be confirmed (DC-005)
- Being demonstrable without real physical sensors or equipment (DC-006, carried over
  from existing text)
- Working on local data without needing constant internet (DC-007, carried over)
- Being achievable in the time and resources available for a course project (DC-008,
  carried over)

**Action:** Replace the current placeholder paragraph in Section 3.5 with these eight
numbered items, keeping a short intro line.

### D. Splitting out a "Performance" list from the "how fast/reliable" list
Right now, one label ("NFR-") is reused for three unrelated things: accuracy, speed,
and general software qualities — which makes it confusing to know which is which.
Six existing speed/capacity items get their own new label (PR-001 to PR-006), and one
new one is added:
- Alerting within 60 seconds of a critical fault (PR-001, was NFR-3)
- Updating the screen within 2 seconds of a new reading (PR-002, was NFR-4)
- Handling at least 10 pieces of equipment at once (PR-003, was NFR-11)
- Handling at least 5 people viewing at once (PR-004, was NFR-12)
- Handling at least 1 reading per second overall (PR-005, was NFR-13)
- Storage sized to hold at least 30 days of readings without discarding early
  (PR-006, was NFR-14)
- **New:** the whole system should be up and actively monitoring within an agreed
  time of being switched on (PR-007) — no number is given yet, so this will be added
  with a placeholder asking the team to agree on a number, exactly as the supporting
  file left it.

**Action:** Renumber these six, add the seventh, and update every place elsewhere in
the document that refers to the old numbers (the verification methods appendix and
the acceptance criteria table).

---

## PART 2 — Handwritten notes found inside the main document itself

| # | Location | What the note says, in plain terms | What will be done |
|---|----------|-------------------------------------|--------------------|
| 1 | Section 2.5 (Assumptions) | Questioned whether "receiving" is the right word, wondering if this should instead point to the requirement covering system interruptions/breakages | Reword the sentence to clearly point to the requirement that already covers what happens when a part of the system is interrupted or broken, instead of just saying "receiving" |
| 2 | FR-10 | Unsure why an explanatory sentence is there; notes this goes to a client and lecturer; asks to "please add" something (unspecified) | Add a plain, one-line note stating this is a stand-in for real connection hardware, so an outside reader (client/lecturer) doesn't mistake the simulated version for a finished product |
| 3 | FR-11 | Asks to "add the other functions" (unspecified) | Covered by the fourteen new items above (FR-16–FR-27), which sit directly on this same topic |
| 4 | Section 3.2 intro | Asks whether the explanation of what a "use case" is, is even necessary | Shorten it to one brief sentence instead of removing it entirely, since first-time readers (client, lecturer) may still need the one-line explanation |
| 5 | NFR-4 | Asks for the 2-second requirement to account for the time a model needs to actually decide something is a fault, not just a blip | Reword the requirement to make clear the 2 seconds includes that decision-making time |
| 6 | NFR-14 / PR-006 | Says the content is good, just wants nicer formatting | Carried over as PR-006 with clean formatting |
| 7 | NFR-8 | Questions whether seeing all equipment on one screen is realistic, since the client wants a laptop screen | Add a short note clarifying this means everything fits on the one laptop dashboard screen without needing extra windows, consistent with the client's stated laptop-based setup |
| 8 | Section 3.7 | Says jumping to Section 5 is awkward and asks why "other requirements" appears twice | Bring the relevant content from Section 5 directly into Section 3.7 itself, so the reader isn't sent elsewhere, and rename Section 5 so the title isn't repeated |
| 9 | NFR-6 | Says the requirement is too long; wants the short, clear rule on top and the explanation below it in italics; also flags NFR-6/6a formatting looks off | Restructure NFR-6 as a short bold rule followed by the explanation in italics underneath. NFR-6a is being moved out entirely (see Part 1A above), which also resolves the formatting confusion |
| 10 | Section 4 | Feels this section is too thin; wants more added covering how the system talks with users and other software, aiming for near-complete coverage | Add plain-language items already implied elsewhere in the document but not yet spelled out here: login/access, the admin change-log, fault records and reports, and time-syncing — nothing beyond what the rest of the document already promises |
| 11 | Section 5.1 (Acceptance Criteria) | Asks to cut down use of the term "F1-score" and use plain English | Reword the acceptance criteria row to describe correctness in plain terms (percentage of faults correctly caught) instead of naming the scoring method; the scoring method itself stays only in the appendix where it's formally defined |

---

## Numbering changes that ripple elsewhere

Because NFR-3, 4, 11, 12, 13, 14 become PR-001–006, and NFR-6a/7a become FR-14/15,
every other place in the document that refers to these old numbers will also be
updated to match, specifically:
- Appendix D (Verification Methods)
- Section 5.1 (Acceptance Criteria table)
- Any other cross-reference found while editing

---

Once you confirm this plan, I will make all these changes directly in the Word
document and show you the result.
