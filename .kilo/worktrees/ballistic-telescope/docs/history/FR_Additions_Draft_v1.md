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

## Flag for Design Constraints (not FR, but raised by the same discussion)
Physical environment differences across reference industries (dust, humidity, heat, electrical interference from heavy machinery) affect sensor accuracy and communication reliability. This should be captured as a **Design Constraint (DC-xxx)**, not a functional requirement — noting it here so it isn't dropped before that section is built.
