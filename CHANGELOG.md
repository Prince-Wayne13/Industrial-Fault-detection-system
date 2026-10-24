# Changelog

One entry per version of the SRS. Newest first. Requirement numbers are those of the version named.

## Unreleased (planned v1.7)

Decided but not yet applied. See `docs/requirement-decisions.md`, part B, for each item against its requirement number.

- Alerts as pop-ups to connected users only. Acknowledging logs who and when (FR-7, FR-8).
- A 10-second window for the trend check. Alert target of 10 seconds (FR-6, PR-001).
- One reading per second for every parameter on every machine (PR-005, PR-006).
- A sanity check before the status model. Raw values still show on the dashboard (FR-14).
- Normal windows keep only status and time stamp. Readings are deleted after a day. Warning and critical windows keep their readings (FR-9, NFR-10).
- Local storage as an active backup. A storage alert at 75% used (FR-20, NFR-6, new requirement).
- New security requirements. Session timeout of 5 minutes, shortened per user (FR-26).
- Roles: the Administrator manages the system and gets no fault alerts. The engineer may change limits, logged.

## v1.6

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
