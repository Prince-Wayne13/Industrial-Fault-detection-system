# Changelog

One entry per version of the SRS. Newest first. Requirement numbers are those of the version named.

## v2.0

Applied to the Word file on 26 October 2026. Wording is in `docs/v2-clear-statements.md`. Numbers stay in page order; new requirements carry a letter (FR-3a, FR-7a, FR-23a, FR-28a and so on).

- Three roles: Operator, Engineer, Administrator. Management / Supervisor dropped. The Operator acknowledges; the Engineer resolves, uses maintenance mode and changes limits; the Administrator manages the system and gets the storage alert (Sections 2.3, 3.1.1, FR-7, FR-8, FR-17, FR-18, FR-21a).
- Alerts as pop-ups to connected Operators and Engineers. Acknowledging logs who and when and does not close the fault (FR-7, FR-8).
- Limits can be changed by the Engineer without a rebuild, with the limit stored on each fault record (FR-23a to FR-23d).
- Security rules: passwords, lockout, HTTPS, stored passwords, 5-minute session timeout with a 1-minute minimum (FR-26, FR-28a to FR-28f).
- One reading per second per parameter. A 10-second window. Normal windows keep status only; their readings are deleted after a day (FR-3a, FR-6, FR-9a, FR-9b, FR-13, NFR-10).
- Status updates every 10 seconds. A critical alert shows within 2 seconds of the status confirming it; a late alert is logged and flagged (PR-001, PR-001a, PR-001b).
- Sizing: at least 40 readings a second and room for 3,456,000 readings (PR-005, PR-006). Start-up time 60 seconds (PR-007). NFR-6 is 99% with local storage as an active backup.
- FR-5: normal or abnormal where only one abnormal level exists. DC-006 and Section 5 say the demonstration is simulated data with fault injection.
- Flask and React with JSX (Appendix B). Cover: version 2.0, date and group members. There is no revision history on the cover, because the 1.x versions never reached the lecturer. Section 1.5 corrected.

Still open: O-4, O-5, O-7, O-9, DD-02. The contents page refreshes when the file is opened in Word (accept the prompt to update fields). Diagrams are not drawn yet.

## v1.6

Versions 1.3 to 1.6 were the team's own working versions. The lecturer saw version 1.1, then 2.0.

- Requirements renumbered in page order. The access-control rules are now FR-27 and FR-28.
- New FR-6: one abnormal reading is not a fault. A check across recent readings comes first.
- UC-2 rewritten with a trend-check step and a one-off-blip alternate flow.
- PR-001 and PR-002 reworded. The design flow note under FR-5 includes the trend check.

## v1.5

- All non-functional requirements merged into Section 3.5. The old Section 3.3 is gone. Sections 3.3 to 3.6 are now Performance, Design Constraints, Software System Attributes and Other Requirements.
- All highlights removed. NFR-6 explanation cut to one sentence. Other long additions trimmed.

## v1.4

- Added FR-14 to FR-27 (fault handling, maintenance mode, storage and recovery, admin log, limit-change history, multiple units, time source, session expiry).
- Added DC-001 to DC-008 and PR-001 to PR-007.
- NFR-6a and NFR-7a moved into the functional list.
- Every margin note resolved. Section 5 renamed Acceptance Criteria. Login, administration, reports and time source added to Section 4.

## v1.3

The document as received, with margin notes. Functional requirements FR-1 to FR-13 and non-functional requirements NFR-1 to NFR-14.
