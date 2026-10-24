# Functional Requirements — Additions & Fixes

## Existing FR-1 to FR-13
Unchanged. Not repeated here.

## Moved from NFR (were miscategorized — these are behaviors, not quality attributes)

**FR-14:** If a piece of equipment stops producing sensor readings for longer than three times its normal reporting interval, the system shall flag that equipment parameter as having a sensor fault and display this on the dashboard, instead of continuing to show the last known reading as current.

**FR-15:** If an incoming reading is of the wrong type, missing, or outside any physically possible range, the system shall reject that specific reading, log it as invalid, and continue operating normally.

## New — Fault Handling

**FR-16:** If two or more parameters on the same equipment become abnormal at the same time, the system shall raise a separate fault record for each affected parameter rather than combining them into a single alert.

**FR-17:** The system shall not raise a duplicate alert for a fault condition that is already open and unacknowledged; it shall only raise a new alert once the condition has returned to normal and then reoccurs.

**FR-18:** The system shall support a fault lifecycle of at least: open → acknowledged → resolved. A user shall be able to mark an acknowledged fault as resolved, and the system shall record when this happens.

## New — Maintenance / Override

**FR-19:** An authorized user shall be able to place a piece of equipment into maintenance mode for a stated duration, during which the system continues recording sensor readings but suspends new fault alerts for that equipment.

**FR-20:** If a piece of equipment remains in maintenance mode beyond its stated duration, the system shall flag this as overdue on the dashboard.

## New — Storage & Recovery

**FR-21:** If the data storage component becomes unavailable or full, the system shall retain new readings in temporary local storage and shall not crash or silently discard data without logging the event.

**FR-22:** On restart after a shutdown or crash, the system shall resume monitoring using the last known configuration and shall not treat equipment status as unknown once fresh readings are received.

## New — Administration & Traceability

**FR-23:** The system shall keep a log of administrative actions (user account changes, equipment registration, threshold/configuration changes), recording who made the change and when.

**FR-24:** If an operating threshold (normal/warning/critical limit) is changed, the system shall retain the previous value and the date of change, rather than overwriting it silently.

## New — Multi-Unit Support

**FR-25:** The system shall support monitoring more than one piece of equipment within the same category (e.g. multiple motors) as separately identifiable units, each with its own status and fault history.

## New — Timing & Sessions

**FR-26:** All system components shall use a synchronized time source, so that fault timestamps and response-time measurements (see Performance Requirements) are consistent across the system.

**FR-27:** A user session shall expire after a period of inactivity, requiring re-authentication before further access.

---

# Design Constraints (new — Section 3.5 currently has no itemized list)

**DC-001:** The system shall be designed on the assumption that monitored equipment operates in industrial environments with significant airborne dust and particulate matter (e.g. sugar dust, flour dust, grain particulate), which can affect sensor accuracy and requires sensors rated for dusty/particulate conditions where physical sensors are used.

**DC-002:** The system shall be designed on the assumption that monitored equipment may operate in environments with high humidity and occasional wash-down water exposure (e.g. breweries, food and beverage processing), which can affect both sensor reliability and electrical/communication connections, requiring appropriately rated (e.g. IP-rated) hardware where physical sensors are used.

**DC-003:** The system shall be designed on the assumption that ambient temperature at monitored sites may reach up to 40°C (per IEC 60034-1) and shall not assume climate-controlled conditions.

**DC-004:** The system shall be designed to tolerate electrical noise and electromagnetic interference from nearby heavy industrial machinery (motors, transformers, switching equipment), which can corrupt sensor readings or disrupt communication links. Noise-handling behavior is addressed functionally in FR-15 (invalid data rejection) and NFR-7 (degraded input handling); this constraint records the environmental cause so it is not lost.

**DC-005:** The system shall be designed without dependence on a specific named industrial site; because sensor specifications for the reference industries (Illovo, Bakhresa, Rab Processors, Universal, Carlsberg, Nyasa) could not all be confirmed, the system uses baseline parameters per Appendix A, adjustable per site during commissioning.

**DC-006:** The system shall be demonstrable without physical sensor hardware or physical access to real industrial equipment (carried over from Section 2.4 — restated here as a formal, numbered constraint rather than prose).

**DC-007:** The system shall remain operable, at least for locally available data, without continuous internet access (carried over from Section 2.4 — restated here as a formal, numbered constraint).

**DC-008:** The project shall be completed within the timeframe and resources available to the group for this course (carried over from Section 2.4 — restated here as a formal, numbered constraint).

---

# Performance Requirements (renumbered — separating PR- from NFR- to fix overloaded numbering)

Currently "NFR-" is reused across three different meanings (Accuracy, Performance, Software System Attributes), which weakens traceability. Recommend giving Performance its own prefix:

**PR-001** *(was NFR-3):* The system shall show a dashboard alert for a critical fault within 60 seconds of that fault occurring, measured from fault injection to alert display.

**PR-002** *(was NFR-4):* The dashboard shall show a newly received sensor reading within 2 seconds, measured from receipt by the processing component to display.

**PR-003** *(was NFR-11):* The system shall support at least 10 pieces of equipment monitored at the same time, across any combination of motors, water pumps, and backup power supplies, without breaching PR-001 or PR-002.

**PR-004** *(was NFR-12):* The system shall support at least 5 dashboard users viewing the system at the same time, without breaching PR-001 or PR-002.

**PR-005** *(was NFR-13):* The system shall be able to receive and process at least 1 sensor reading per second across all monitored equipment combined, without breaching PR-001 or PR-002.

**PR-006** *(was NFR-14):* Given 10 pieces of equipment, 3 monitored parameters each, readings taken once per minute, and a 30-day retention period, the data store shall be sized to hold at least 1,296,000 readings without needing to discard data early.

**New — PR-007:** All system components shall complete startup and be actively monitoring equipment within [X seconds/minutes — value to be agreed] of launch.

---

# Summary of what changes in the document

1. **Section 3.1 Functional Requirements** — add FR-14 through FR-27. Remove NFR-6a and NFR-7a from Section 3.6 (superseded by FR-14/FR-15).
2. **Section 3.4 Performance Requirements** — replace NFR-3/4/11/12/13/14 with PR-001 to PR-007. Update every cross-reference elsewhere in the document (Appendix D, Section 5 acceptance criteria) that currently cites these by their old NFR numbers.
3. **Section 3.5 Design Constraints** — replace the current single paragraph with DC-001 to DC-008 (itemized), keeping the paragraph as a short intro line if useful.
4. **Section 3.6 Software System Attributes** — remove NFR-6a and NFR-7a (moved to FR-14/FR-15 above); NFR-5, NFR-6, NFR-7, NFR-8, NFR-9, NFR-10 stay as-is here since they are genuine quality attributes, not behaviors.
