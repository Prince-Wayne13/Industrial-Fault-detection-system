**Software Requirements Specification**

for

**Industrial Fault Detection System for Motors, Water Pumps, and Backup Power Supplies**

**Version 2.0**

Prepared by Group 3 BEEE

Group members: Prince Msowoya, Zilpah Kalipa, Theresa Somanje, Opra Chikwangwala, Steven Nkhoma, Akuzike Mphande, Timothy Kaperenganya

26-10-2026

# **Table of Contents**

[Table of Contents](#table-of-contents)

[1. Introduction](#introduction)

[**1.1 Purpose**](#purpose)

[**1.2 Scope**](#scope)

[**1.3 Definitions, Acronyms, and Abbreviations**](#definitions-acronyms-and-abbreviations)

[**1.4 References**](#references)

[**1.5 Overview**](#overview)

[2. Overall Description](#overall-description)

[**2.1 Product Perspective**](#product-perspective)

[**2.2 Product Functions**](#product-functions)

[**2.3 User Characteristics**](#user-characteristics)

[**2.4 Constraints**](#constraints)

[**2.5 Assumptions and Dependencies**](#assumptions-and-dependencies)

[3. Specific Requirements](#specific-requirements)

[**3.1 Functional Requirements**](#functional-requirements)

[**Equipment Monitoring**](#equipment-monitoring)

[**Fault Detection**](#fault-detection)

[**Fault Alerts and Notifications**](#fault-alerts-and-notifications)

[**Fault Recording and Reporting**](#fault-recording-and-reporting)

[**Remote Monitoring and Connectivity**](#remote-monitoring-and-connectivity)

[**Access Control**](#access-control)

[**3.1.1 User Role Permissions**](#user-role-permissions)

[**3.2 Use Cases**](#use-cases)

[**UC-1: Monitor Equipment Status**](#uc-1-monitor-equipment-status)

[**UC-2: Detect a Fault and Alert the User**](#uc-2-detect-a-fault-and-alert-the-user)

[**UC-3: Review Fault History and Generate a Report**](#uc-3-review-fault-history-and-generate-a-report)

[**UC-4: Continue Monitoring During a Connection Interruption**](#uc-4-continue-monitoring-during-a-connection-interruption)

[**UC-5: Administer Users and Equipment**](#uc-5-administer-users-and-equipment)

[**UC-6: Place Equipment in Maintenance Mode**](#uc-6-place-equipment-in-maintenance-mode)

[**3.3 Performance Requirements**](#_Toc241385505)

[**Response Time**](#response-time)

[**Capacity**](#capacity)

[**3.4 Design Constraints**](#design-constraints)

[**3.5 Software System Attributes**](#software-system-attributes)

[**Reliability**](#reliability)

[**Usability**](#usability)

[**Maintainability**](#maintainability)

[**Data Retention**](#data-retention)

[**3.6 Other Requirements**](#other-requirements)

[4. External Interface Requirements](#external-interface-requirements)

[**4.1 User Interface**](#user-interface)

[**4.2 Hardware Interface**](#hardware-interface)

[**4.3 Software Interface**](#software-interface)

[**4.4 Communication Interface**](#communication-interface)

[5. Acceptance Criteria](#acceptance-criteria)

[Appendix A: Reference Operating Limits](#appendix-a-reference-operating-limits)

[**A.1 Induction Motor — IEC 60034-1 / ISO 10816-3 (current, vibration); Team-Selected (temperature)**](#a.1-induction-motor-iec-60034-1-iso-10816-3-current-vibration-team-selected-temperature)

[**A.2 Water Pump — Manufacturer Specification (Dayliff) + International Standard (ISO 9906)**](#a.2-water-pump-manufacturer-specification-dayliff-international-standard-iso-9906)

[**A.3 Backup Power Supply / UPS: Team-Selected Working Values**](#a.3-backup-power-supply-ups-team-selected-working-values)

[**A.4 Other Team-Selected Working Values**](#a.4-other-team-selected-working-values)

[**Motor RPM threshold (team-selected)**](#motor-rpm-threshold-team-selected)

[**Water pump: bearing temperature, current, vibration and RPM (team-selected)**](#water-pump-bearing-temperature-current-vibration-and-rpm-team-selected)

[**Motor temperature (team-selected)**](#motor-temperature-team-selected)

[Appendix B: Design Decisions](#appendix-b-design-decisions)

[Appendix C: Open Items and Known Limitations](#appendix-c-open-items-and-known-limitations)

[**Values not backed by a cited source**](#values-not-backed-by-a-cited-source)

[**Design-stage items**](#design-stage-items)

[**Verification status**](#verification-status)

[**Final Implementation Check Before Submission**](#final-implementation-check-before-submission)

[Appendix D: Verification Methods](#appendix-d-verification-methods)

# **1. Introduction**

## **1.1 Purpose**

Industrial equipment such as motors, water pumps, and backup power supplies often fail suddenly, without warning, causing damage and downtime that could have been reduced with earlier detection. This document specifies what the system must accomplish and the limits it must operate within, in order to continuously monitor such equipment, detect abnormal operating conditions before failure occurs, and alert responsible personnel in time to act.

This document specifies requirements only — what the system must do. How those requirements are technically achieved (specific tools, languages, and platforms) is recorded separately in Appendix B: Design Decisions, and is not part of the requirements themselves.

## **1.2 Scope**

The system shall monitor three categories of industrial equipment — induction motors, water pumps, and backup power supplies — by collecting sensor data, comparing it against defined operating limits, detecting abnormal conditions, and alerting responsible personnel.

The system is intended to be general enough that the same monitoring, fault-detection, and alerting requirements could apply to similar equipment in other industries, not only the specific machines used in this implementation.

For this implementation, sensor data is generated using a simulation rather than physical sensor hardware, as recorded in Section 2.5 (Assumptions and Dependencies). This is a stated method of satisfying the requirements below, not a change to the requirements themselves.

Out of scope: physical sensor installation and calibration; validation of fault-detection behavior against real (non-simulated) equipment; hardware procurement or deployment.

## **1.3 Definitions, Acronyms, and Abbreviations**

| **Term** | **Definition**                                                                                                                  |
|----------|---------------------------------------------------------------------------------------------------------------------------------|
| Fault    | A sensor reading or pattern of readings classified by the system as an abnormal operating condition requiring attention.        |
| Warning  | A fault severity level indicating a parameter has exceeded its normal range but not yet reached a critical level.               |
| Critical | A fault severity level indicating a parameter has reached a level associated with imminent risk of equipment damage or failure. |
| TTD      | Time-to-Detect: the time between a fault condition occurring and the system identifying it as a fault.                          |
| TTA      | Time-to-Alert: the time between a fault being identified and an alert being generated for the user.                             |
| MTBF     | Mean Time Between Failures: a reliability metric describing the average operating time between system failures.                 |
| FLA      | Full Load Amps: the rated current draw of a motor operating at its full rated load.                                             |

## **1.4 References**

- IEC 60034-1:2022 — Rotating Electrical Machines, Part 1: Rating and Performance. International Electrotechnical Commission.

- ISO 10816-3:2009 — Mechanical vibration — Evaluation of machine vibration by measurements on non-rotating parts, Part 3.

- Industrial Monitor Direct — 3-Phase Induction Motor Temperature Ratings: Class B, F, H Guide.

- Malawi Bureau of Standards (MBS) — National Standards Body of Malawi; ISO member body and IEC affiliate country. See www.mbsmw.org and https://www.iso.org/member/1921.html.

- Davis & Shirtliff / Dayliff — DDP Series Peripheral Pump Datasheet (max fluid temperature +60°C, max ambient temperature +40°C). Davis & Shirtliff Ltd, Nairobi. Regional supplier with confirmed Malawi market presence. See www.davisandshirtliff.com and www.dayliff.com.

- ISO 9906 — Rotodynamic pumps — Hydraulic performance acceptance tests. Referenced as the applicable pump-performance testing standard (confirmed via Wilo SE's ISO 9906 Grade 1B test bench for the East Africa region).

Note on national standards applicability: MBS is Malawi's national standards body and operates as a full ISO member and IEC affiliate. MBS does not author separate national equipment standards competing with IEC/ISO in this domain — international standards (as cited above) apply directly. This is stated explicitly here rather than left as a gap, since a reviewer may otherwise ask why no distinct Malawian standard is cited.

Note on motor temperature limits: the motor temperature limits used by this specification (normal below 120°C, warning above 130°C, critical above 150°C) are team-selected working values, pending equipment-specific validation. They are not taken directly from IEC 60034-1. An earlier table using a different arrangement of the same figures was reconciled to these values by the group. See Appendix A.1 and A.4.

Note on backup power supply parameters: no manufacturer datasheet or standard has been identified for equipment-level UPS operating parameters. The values in Appendix A.3 are therefore team-selected working values, pending equipment-specific validation. Malawi's grid-instability context (ESCOM load shedding and ESCOM's 20 MW Battery Energy Storage System in Lilongwe, see Section 2.1) is cited only as framing for why backup power monitoring matters; it is grid-scale infrastructure data and is not used as a source for equipment-level limits.

## **1.5 Overview**

Section 2 describes the system at a high level: its context, its main functions, its intended users, and the assumptions and constraints it operates under. Section 3 specifies detailed, testable requirements. Section 4 specifies external interface requirements. Section 5 sets out the acceptance criteria, which are checked in the final demonstration. Section 3.6 covers other requirements. Appendix B records the design decisions made to satisfy these requirements, kept separate from the requirements themselves.

# **2. Overall Description**

## **2.1 Product Perspective**

The system consists of a data source representing the monitored equipment (motor, water pump, backup power supply), a processing component that evaluates incoming data against defined limits and classifies conditions, a data store, and a monitoring dashboard used by personnel.

For this implementation, the equipment data source is a simulation rather than physical sensor hardware. This substitution is recorded as an assumption in Section 2.5 and does not change what the processing, storage, and dashboard components are required to do.

Backup power monitoring is a genuine, current requirement in this context: Malawi's national grid operator (ESCOM) runs an active, published load-shedding program, and has itself recently deployed a 20-megawatt grid-scale Battery Energy Storage System to reduce outage duration — confirming that power instability and battery/backup reliance are real, present-day operating conditions for equipment in this environment, not a hypothetical scenario.

## **2.2 Product Functions**

At a high level, the system shall:

- Monitor motor, water pump, and backup power supply operating conditions

- Detect abnormal operating conditions by comparing measurements against defined operating limits

- Store sensor measurements and detected faults

- Display current equipment status and historical data on a dashboard

- Alert responsible personnel when a fault is detected

- Support remote monitoring under intermittent connectivity

- Support different levels of access for different categories of users

## **2.3 User Characteristics**

| **User Category** | **Characteristics and System Needs**                                                                                                                                                                                                                                                                                                                                                               |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Operator          | Basic to moderate technical knowledge. The first responder on shift: monitors motor and pump operating conditions during production, sees fault alerts, acknowledges them and can generate reports. Needs a simple dashboard showing measurements, machine status, and clear warning/critical alerts. Does not resolve faults, use maintenance mode, change limits or change system configuration. |
| Engineer          | Technical knowledge of industrial motors, pumps, electrical systems, and maintenance, and often working remotely. Diagnoses and fixes faults. Does everything an Operator does, and also marks faults resolved, places equipment in maintenance mode and changes limits (every change is logged).                                                                                                  |
| Administrator     | Knowledge of the software and basic IT/network administration. Manages user accounts, access permissions, equipment registration, system settings and data storage, and receives the storage alert. Is not an operational user: receives no fault alerts and does not acknowledge faults.                                                                                                          |

The system has three roles because it gives three different sets of rights: watching and acknowledging faults (Operator), fixing faults and tuning limits (Engineer), and managing the system (Administrator).

## **2.4 Constraints**

The following are real-world restrictions that limit the system's possible solutions, rather than technical choices made to satisfy a requirement (see Appendix B for those):

- The system must be demonstrable without physical sensor hardware or physical access to real industrial equipment.

- The system must remain operable, at least for locally available data, without continuous internet access.

- The project must be completed within the timeframe and resources available to the group for this course.

## **2.5 Assumptions and Dependencies**

The following assumptions and dependencies define the conditions under which the system is expected to operate correctly:

- Simulated sensor data is assumed to be representative of real sensor behavior under normal and fault conditions, including realistic noise and response characteristics. Validation against real physical sensor data is outside the scope of this project.

- A fault-classification capability is assumed to be trainable using labeled data derived from simulation, including intentionally generated fault conditions. Its performance depends on how representative these simulated fault scenarios are of real equipment behavior.

- Correct operating limits (temperature, vibration, current, voltage, etc.) depend on appropriate values for the specific equipment class, obtained from manufacturer guidance and relevant standards, as listed in Section 1.4.

- The system depends on its data-processing and storage components functioning correctly for storing and retrieving measurements and fault records, and on the interruption-handling behaviour defined in FR-20 and FR-21 when a component is temporarily unavailable.

- Users are assumed to have valid accounts and appropriate permissions corresponding to the roles defined in Section 2.3.

- The system is designed to continue operating on locally available data if communication between system components is temporarily interrupted, and to resume full operation once it is restored.

The specific mechanism used to stream simulated data to the processing component is a design decision and is recorded in Appendix B. Any dependency of that mechanism on a specific tool or toolbox is a design-stage risk, and is listed in Appendix C.

# **3. Specific Requirements**

## **3.1 Functional Requirements**

### **Equipment Monitoring**

FR-1: The system shall monitor motor operating conditions, including temperature, current, vibration, and rotational speed (RPM).

FR-2: The system shall monitor water pump operating conditions, including bearing temperature, current draw, vibration, and rotational speed (RPM).

FR-3: The system shall monitor backup power supply/UPS operating conditions, including internal temperature, charging/output current, and cooling fan speed.

*Note: the pump bearing-temperature, current and vibration limits, and all backup power supply limits, are team-selected working values (see Appendix A.2 to A.4). They are adopted for the simulation and are pending equipment-specific validation.*

FR-3a: The system shall take one reading per second for every monitored parameter on every machine.

### **Fault Detection**

FR-4: The system shall compare incoming measurements against the defined operating limits for the corresponding equipment and parameter and flag measurements or patterns that exceed those limits.

FR-5: For conditions flagged by FR-4, the system shall classify the condition as normal, warning, or critical using the defined fault-classification method and identify the affected equipment and parameter. Where the limits define only one abnormal level, the system shall classify the condition as normal or abnormal.

FR-6: A condition flagged by FR-4 shall not be classified as a fault under FR-5 based on a single abnormal reading alone. The system shall first check whether the abnormal condition holds across the readings of the latest 10-second window for that parameter; only if it does shall FR-5 classification and the FR-7 alert proceed. A single abnormal reading that does not repeat is not treated as a fault, and the dashboard's live reading (see NFR-8) is unaffected either way.

Design clarification (Appendix B): the processing flow is simulated sensor data → threshold screening → flagged abnormal condition → trend check (FR-6) → fault classification/severity assignment → fault record → dashboard alert. The logistic-regression model performs the classification stage; it does not replace the initial threshold screening or the trend check.

### **Fault Alerts and Notifications**

FR-7: When the status model confirms a fault, the system shall show a pop-up alert to every connected Operator and Engineer, whether near-range or remote.

FR-7a: The pop-up shall show the equipment, the parameter, the fault type, the severity and the time.

FR-7b: The system shall not send fault alerts to the Administrator.

FR-7c: If no Operator or Engineer is connected, the fault shall stay open and be shown to the next Operator or Engineer who connects.

FR-8: An Operator or Engineer shall be able to acknowledge an open fault from its alert.

FR-8a: When a fault is acknowledged, the system shall record which user did it and when.

FR-8b: Acknowledging shall not close the fault. It stays open until an Engineer marks it resolved (FR-17).

### **Fault Recording and Reporting**

FR-9: The system shall record detected faults and sensor readings for later retrieval.

FR-9a: For every 10-second window, the system shall store the status and its time stamp.

FR-9b: The readings of a normal window shall be deleted after 24 hours. The readings of a warning or critical window shall be kept with their status.

FR-10: All users shall be able to view fault history. Operators and Engineers shall be able to generate reports from fault history showing equipment performance and recurring faults.

### **Remote Monitoring and Connectivity**

FR-11: The system shall support both a near-range and a remote-range connection mode for accessing equipment data from the dashboard. The final demonstration shall provide a selectable simulated mode for each connection type.

This removes the unnecessary requirement to calculate physical proximity while still demonstrating both connection scenarios. Both modes are simulated, as a stand-in for physical connection hardware (see Section 1.2).

FR-12: The system shall continue collecting, evaluating, and displaying locally available equipment status if the connection between system components is temporarily interrupted, and shall store any data collected during the interruption for transmission once the connection is restored.

### **Fault Handling**

FR-13: If no reading arrives for a parameter for 3 seconds, the system shall flag that parameter as having a sensor fault and display this on the dashboard, instead of continuing to show the last known reading as current.

FR-14: If an incoming reading is of the wrong type, missing, or outside any physically possible range, the system shall reject that specific reading, log it as invalid, and continue operating normally.

FR-15: If two or more parameters on the same equipment become abnormal at the same time, the system shall raise a separate fault record for each affected parameter rather than combining them into a single alert.

FR-16: The system shall not raise a duplicate alert for a fault condition that is already open and unacknowledged; it shall only raise a new alert once the condition has returned to normal and then reoccurs.

FR-17: The system shall support a fault lifecycle of at least: open → acknowledged → resolved. An Engineer shall be able to mark an acknowledged fault as resolved, and the system shall record when this happens.

### **Maintenance / Override**

FR-18: An Engineer shall be able to place a piece of equipment into maintenance mode for a stated duration, during which the system continues recording sensor readings but suspends new fault alerts for that equipment.

FR-19: If a piece of equipment remains in maintenance mode beyond its stated duration, the system shall flag this as overdue on the dashboard.

### **Storage & Recovery**

FR-20: If the data storage component becomes unavailable or full, the system shall retain new readings in temporary local storage and shall not crash or silently discard data without logging the event.

FR-21: On restart after a shutdown or crash, the system shall resume monitoring using the last known configuration and shall not treat equipment status as unknown once fresh readings are received.

FR-21a: When storage use reaches 75%, the system shall send an alert to the Administrator only. The Administrator manages storage.

### **Administration & Traceability**

FR-22: The system shall keep a log of administrative actions (user account changes, equipment registration, threshold/configuration changes), recording who made the change and when.

FR-23: If an operating threshold (normal/warning/critical limit) is changed, the system shall retain the previous value and the date of change, rather than overwriting it silently.

FR-23a: An Engineer shall be able to change the warning limit and the critical limit for any parameter of any equipment type, from the dashboard, without restarting or rebuilding the system.

FR-23b: The system shall reject a new limit if the warning limit is not below the critical limit.

FR-23c: A changed limit shall apply to readings received after the change.

FR-23d: Each fault record shall store the limit that was in force when the fault was raised.

### **Multi-Unit Support**

FR-24: The system shall support monitoring more than one piece of equipment within the same category (e.g. multiple motors) as separately identifiable units, each with its own status and fault history.

### **Timing & Sessions**

FR-25: All system components shall use a synchronized time source, so that fault timestamps and response-time measurements (see Section 3.3, Performance Requirements) are consistent across the system.

FR-26: A user session shall expire after 5 minutes of inactivity, requiring re-authentication before further access. A user may set a shorter time, but not shorter than 1 minute and not longer than 5 minutes.

### **Access Control**

FR-27: The system shall restrict configuration, user-account management, and equipment-registration functions to users in the Administrator role.

FR-28: The system shall require authentication before allowing access to any monitoring or administrative function.

FR-28a: Passwords shall be at least 15 characters long, and the system shall accept passwords of 64 characters or more.

FR-28b: The system shall not require a mix of capitals, numbers or symbols in a password, and shall not force password changes on a schedule.

FR-28c: The system shall refuse passwords that appear on a list of common or leaked passwords.

FR-28d: After 5 failed login attempts on an account, the system should block login to that account for 15 minutes.

FR-28e: All communication between the dashboard and the server shall use HTTPS (TLS 1.2 or newer).

FR-28f: The system shall store passwords only in a salted, hashed form that cannot be read back.

### **3.1.1 User Role Permissions**

The permissions below apply FR-8, FR-10, FR-17, FR-18, FR-23a and FR-27. The system has three roles because it gives three different sets of rights: watching and acknowledging faults (Operator), fixing faults and tuning limits (Engineer), and managing the system (Administrator).

| **Function**                                                         | **Operator** | **Engineer** | **Administrator** |
|----------------------------------------------------------------------|--------------|--------------|-------------------|
| View equipment status, readings and fault history                    | Yes          | Yes          | Yes               |
| See fault pop-ups                                                    | Yes          | Yes          | No                |
| Acknowledge a fault                                                  | Yes          | Yes          | No                |
| Mark a fault resolved                                                | No           | Yes          | No                |
| Put equipment in maintenance mode                                    | No           | Yes          | No                |
| Change limits                                                        | No           | Yes          | No                |
| Generate reports from fault history                                  | Yes          | Yes          | No                |
| Manage accounts, equipment registration, system settings and storage | No           | No           | Yes               |
| Receive the 75% storage alert                                        | No           | No           | Yes               |

## **3.2 Use Cases**

This section describes how each type of user works with the system to reach a goal, showing the behaviour that supports the functional requirements in Section 3.1.

### **UC-1: Monitor Equipment Status**

**Primary Actor:** Operator

**Goal:** See the current condition of the motor, water pump, and backup power supply at a glance

**Preconditions:** The user has a valid account and is logged in. At least one piece of equipment is registered in the system.

**Main Success Scenario**

1.  The user opens the dashboard.

2.  The system shows the current status of every registered piece of equipment (normal, warning, or critical).

3.  The user selects a specific piece of equipment to see more detail.

4.  The system shows the current sensor readings and recent history for that equipment.

**Alternate / Exception Flows**

- 2a. No equipment is registered yet: the system shows a clear empty-state message instead of a blank or broken screen.

- 2b. A sensor has stopped reporting: the system marks that parameter as "sensor fault" rather than showing an old reading as if it were current (see FR-13).

- 4a. No historical data exists yet for newly registered equipment: the system shows current readings only and states that history will build up over time.

### **UC-2: Detect a Fault and Alert the User**

**Primary Actor: System (initiated automatically); Secondary Actor: Operator or Engineer**

**Goal:** Warn a user in time for them to act, whenever equipment moves outside its normal operating range

**Preconditions:** The equipment is registered and its normal operating limits are configured. The system is actively receiving sensor data for it.

**Main Success Scenario**

1.  The system receives a new sensor reading.

2.  The system compares the reading against the defined operating limits for that equipment and parameter.

3.  The reading falls outside the normal range.

4.  The system checks whether the abnormal condition holds across recent readings for that parameter (FR-6), to rule out a one-off sensor blip.

5.  The condition holds, so the system classifies it as warning or critical.

6.  The system creates a fault record and raises an alert on the dashboard, showing the equipment, the parameter, and the severity.

7.  The user sees the alert and acknowledges it.

**Alternate / Exception Flows**

- 3a. The reading is within normal range: the system takes no further action and continues monitoring.

- 4a. The condition does not hold across the recent readings checked under FR-6: the system treats this as a one-off blip, not a fault, and takes no further action.

- 6a. Two or more parameters on the same equipment are abnormal at the same time: the system raises a separate fault record for each affected parameter rather than merging them into one unclear alert.

- 6b. The same fault condition continues on the next reading: the system does not raise a duplicate alert for a fault that is already open and unacknowledged.

- 7a. No user acknowledges the alert: the fault remains visible on the dashboard as open until it is acknowledged or the condition returns to normal.

### **UC-3: Review Fault History and Generate a Report**

**Primary Actor: Operator or Engineer**

**Goal:** Understand how a piece of equipment has been performing over time and spot recurring problems

**Preconditions:** The user is logged in and has permission to view fault history.

**Main Success Scenario**

1.  The user opens the fault history for a piece of equipment.

2.  The system shows past faults for that equipment, including when each one happened and how it was resolved.

3.  The user chooses a date range and asks for a report.

4.  The system generates a report showing equipment performance and any recurring faults over that period.

**Alternate / Exception Flows**

- 2a. No faults have occurred in the selected period: the system states this clearly rather than showing an empty table with no explanation.

- 3a. The user selects a date range with no data at all (for example, before the equipment was registered): the system explains why no report can be produced.

### **UC-4: Continue Monitoring During a Connection Interruption**

**Primary Actor:** System (initiated automatically)

**Goal:** Keep collecting and showing equipment data even when the connection between system components is temporarily lost

**Preconditions:** The system is actively monitoring equipment when the interruption begins.

**Main Success Scenario**

1.  The connection between the data source and the processing component is lost.

2.  The system continues collecting whatever data is still locally available and keeps showing it on the dashboard.

3.  The system stores newly generated readings locally instead of discarding them.

4.  The connection is restored.

5.  The system sends the stored readings to the central database and resumes normal operation.

**Alternate / Exception Flows**

- 1a. The interruption is at the sensor itself rather than the network: the system treats this as a sensor fault (UC-1, 2b), not as a connection interruption.

- 3a. The interruption lasts longer than local storage can hold: the oldest stored readings are discarded first, and the system logs this as an extended outage rather than silently losing data without a record.

- 5a. Some stored readings cannot be sent after reconnection (for example, they are corrupted): the system discards them under the same rule used for corrupted live readings, and this is logged rather than blocking the rest of the sync.

### **UC-5: Administer Users and Equipment**

**Primary Actor:** Administrator

**Goal:** Control who can use the system and what equipment it monitors

**Preconditions:** The user is logged in with the Administrator role.

**Main Success Scenario**

1.  The administrator opens the administration area.

2.  The administrator adds, edits, or removes a user account, or registers a new piece of equipment.

3.  The system applies the change and records who made it and when.

**Alternate / Exception Flows**

- 1a. A user without the Administrator role tries to open the administration area: the system denies access (see FR-27, FR-28).

- 2a. The administrator tries to remove a user or piece of equipment that is referenced by existing fault history: the system keeps the historical records intact and does not silently delete data tied to them.

### **UC-6: Place Equipment in Maintenance Mode**

**Primary Actor:** Engineer

**Goal:** Work on a piece of equipment (for example, testing a pump while it is intentionally run dry) without the system raising false alerts

**Preconditions:** The user is logged in and has permission to change equipment status. The equipment is currently being monitored normally.

**Main Success Scenario**

1.  The Engineer selects a piece of equipment and places it in maintenance mode, stating an expected duration.

2.  The system stops raising new alerts for that equipment while still recording its readings.

3.  The Engineer completes the work and takes the equipment out of maintenance mode.

4.  The system resumes normal fault detection for that equipment.

**Alternate / Exception Flows**

- 1a. The stated duration passes and the Engineer has not ended maintenance mode: the system flags this on the dashboard as overdue rather than leaving the equipment silently unmonitored.

- 2a. A reading during maintenance mode is severe enough to suggest a safety risk rather than an expected test condition: this case is noted as an open item in Appendix C, since the exact threshold for overriding maintenance mode needs to be confirmed with the client.

## **3.3 Performance Requirements**

This section states both how fast the system must respond (dynamic behaviour) and how much it must be able to handle at once (capacity, which stays fixed regardless of load).

### **Response Time**

PR-001: The system shall update the status of each machine at least every 10 seconds.

PR-001a: When the status is critical, the system shall show the alert immediately after the status confirms it, and no later than 2 seconds afterwards. A single abnormal reading never raises an alert (FR-6).

PR-001b: If an alert is shown more than 2 seconds after its status confirms the fault, the system shall still show the alert, write the delay to the log, and show an "alerts delayed" notice on the dashboard.

*The alert is late only when part of the system is interrupted or slow. The fault is still recorded and stays open, and is shown to the next user who connects. The cost of lateness is that the equipment runs longer before anyone acts.*

PR-002: The dashboard shall show a newly received sensor reading within 2 seconds. The 2 seconds is counted from the moment the processing component receives the reading to the moment it appears on the dashboard, and applies to displaying the reading itself; it does not include the FR-6 trend check that decides whether a warning or critical alert is raised (see PR-001).

### **Capacity**

PR-003: The system shall support at least 10 pieces of equipment monitored at the same time, across any combination of motors, water pumps, and backup power supplies, without breaching PR-001 or PR-002.

PR-004: The system shall support at least 5 dashboard users viewing the system at the same time, without breaching PR-001 or PR-002.

PR-005: The system shall process at least one reading per second for every monitored parameter on every machine, and at least 40 readings per second in total (10 machines × 4 parameters). If a machine has extra parameters, the system shall still keep up, without breaching PR-001 or PR-002.

PR-006: The system shall have room for at least 3,456,000 readings (one day at the minimum load), plus statuses and fault records. (10 machines × 4 parameters × 86,400 seconds in a day. Each extra parameter on 10 machines adds 864,000 a day.)

PR-007: All system components shall complete startup and be actively monitoring equipment within 60 seconds of launch.

## **3.4 Design Constraints** 

This section lists the real-world conditions and limits the system's design must work within.

- DC-001: The system shall be designed on the assumption that monitored equipment operates in industrial environments with significant airborne dust and particulate matter (e.g. sugar dust, flour dust, grain particulate), which can affect sensor accuracy and requires sensors rated for dusty/particulate conditions where physical sensors are used.

- DC-002: The system shall be designed on the assumption that monitored equipment may operate in environments with high humidity and occasional wash-down water exposure (e.g. breweries, food and beverage processing), which can affect both sensor reliability and electrical/communication connections, requiring appropriately rated (e.g. IP-rated) hardware where physical sensors are used.

- DC-003: The system shall be designed on the assumption that ambient temperature at monitored sites may reach up to 40°C (per IEC 60034-1) and shall not assume climate-controlled conditions.

- DC-004: The system shall be designed to tolerate electrical noise and electromagnetic interference from nearby heavy industrial machinery (motors, transformers, switching equipment), which can corrupt sensor readings or disrupt communication links. Noise-handling behaviour is addressed functionally in FR-14 (invalid data rejection) and NFR-7 (degraded input handling); this constraint records the environmental cause so it is not lost.

- DC-005: The system shall be designed without dependence on a specific named industrial site; because sensor specifications for the reference industries could not all be confirmed, the system uses baseline parameters per Appendix A, adjustable per site during commissioning.

- DC-006: The system shall be demonstrable without physical sensor hardware or physical access to real industrial equipment. The system is demonstrated with simulated sensor data and a fault-injection mode, and all tests are run on that simulation.

- DC-007: The system shall remain operable, at least for locally available data, without continuous internet access.

- DC-008: The project shall be completed within the timeframe and resources available to the group for this course.

## **3.5 Software System Attributes**

### **Accuracy**

NFR-1: The system shall correctly identify at least 95% of critical faults (temperature and current problems), measured on the labelled simulated test set described in Appendix D.

NFR-2: The system shall correctly identify at least 85% of vibration-based faults, measured on the same labelled simulated test set described in Appendix D.

### **Reliability**

NFR-5: The system shall keep a record of its own uptime during each test session. During the demonstration, the data-logging function shall be running for at least 95% of the session, not counting planned restarts that the team carries out on purpose (for example, to reload configuration).

NFR-6: The system shall store at least 99% of the sensor readings its data source generates, including during a connection interruption. The local store records the same readings at the same time as the main store, and the same keep and delete rules apply to both.

*A reading only counts as "lost" if it was generated by the equipment's data source but never reaches the central database; readings never produced (FR-13) or discarded as invalid (NFR-7) don't count against this limit.*

NFR-7: The system shall keep producing valid, uncorrupted readings when the input data is noisy or degraded, or shall identify and discard any reading it cannot validate rather than passing it on or acting on it.

### **Usability**

NFR-8: A user shall be able to see the current status of every piece of monitored equipment from the main dashboard on a single laptop screen, without having to open a second window.

### **Maintainability**

NFR-9: The system shall be built so that the monitoring logic for one equipment type or one parameter can be changed on its own, without needing changes to unrelated parts of the system.

### **Data Retention**

NFR-10: The system shall keep statuses and warning or critical records until storage use reaches 75%, and shall never delete them automatically. The readings of normal windows are deleted after 24 hours (FR-9b).

## **3.6 Other Requirements**

Legal and regulatory, data retention, and environmental requirements that apply to the whole system, rather than to one equipment category, are as follows:

- Legal/regulatory: The system shall comply with applicable electrical safety requirements for any physical equipment referenced in its design.

- Data retention: as specified in NFR-10 (above).

- Environmental: The equipment thresholds used by the system (Appendix A) shall be appropriate to the environmental conditions of the monitored equipment; where those conditions are not yet known or confirmed, they are identified in Appendix A.

# **4. External Interface Requirements**

## **4.1 User Interface**

The dashboard shall display machine status, current sensor values, fault alerts, and historical graphs.

The system shall allow users to view equipment status, view detected faults and their details, view current and historical sensor readings, and acknowledge fault notifications.

The system shall require a user to log in before showing any part of the dashboard (see FR-28). An Administrator shall manage user accounts, equipment registration and system settings, and an Engineer shall manage maintenance mode and limits, through the same interface (see FR-27, FR-18, FR-23a).

The system shall allow Operators and Engineers to generate, and all users to view, fault-history reports for a chosen equipment and date range (see FR-10, UC-3).

## **4.2 Hardware Interface**

The system shall receive equipment measurements (temperature, vibration, current, voltage, and other relevant parameters) from a data source representing each piece of monitored equipment, in a form suitable for processing regardless of whether that source is physical sensor hardware or a substitute data source, as described in Section 2.5.

## **4.3 Software Interface**

The system shall store and retrieve sensor measurements and fault records through a data storage component.

## **4.4 Communication Interface**

The system shall transmit sensor measurements from the equipment data source to the processing component.

The system shall transmit processed equipment status, fault alerts, and historical data from the processing component to the dashboard.

All communication interfaces shall use a synchronized time source, consistent with FR-25, so that timestamps recorded by different components agree with one another.

# **5. Acceptance Criteria**

Each criterion below is demonstrated during the final demonstration, using simulated sensor data and a fault-injection mode, and is traceable to the requirements listed against it.

| **ID** | **Acceptance Criterion**                                                                                                                                                          | **Requirements**      |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| AC-1   | A simulated critical fault produces a dashboard alert within 2 seconds of its status confirming it, and each machine's status updates at least every 10 seconds.                  | PR-001, PR-001a, FR-7 |
| AC-2   | An Administrator can perform configuration, user-management and equipment-registration actions; a user in any other role cannot.                                                  | FR-27, FR-28          |
| AC-3   | During a simulated communication interruption, locally generated data is retained and is synchronized after reconnection, with no more than 1% of records lost.                   | FR-12, NFR-6          |
| AC-4   | The required sensor parameters for motors, water pumps and backup power supplies are displayed on the dashboard and stored.                                                       | FR-1 to FR-3, FR-9    |
| AC-5   | The system correctly catches the target share of faults set out in NFR-1 and NFR-2, measured on the held-out labeled simulated test set.                                          | NFR-1, NFR-2          |
| AC-6   | The demonstration can switch between the simulated near-range and remote-range modes and receive/display equipment data in each mode.                                             | FR-11                 |
| AC-7   | An Engineer can change a warning or critical limit from the dashboard without restarting the system. A new limit whose warning value is not below its critical value is rejected. | FR-23a, FR-23b        |
| AC-8   | An alert shown more than 2 seconds late is still shown, is written to the log, and the dashboard shows an "alerts delayed" notice.                                                | PR-001b               |

# **Appendix A: Reference Operating Limits**

This appendix records the specific parameter values referenced by the requirements in Section 3. It is reference data supporting the requirements, not the requirements themselves. Figures are grouped by whether they trace to a named, verifiable source (A.1–A.2) or are team-selected working values pending equipment-specific validation (A.3–A.4).

## **A.1 Induction Motor — IEC 60034-1 / ISO 10816-3 (current, vibration); Team-Selected (temperature)**

| **Parameter** | **Normal**      | **Warning** | **Critical**      |
|---------------|-----------------|-------------|-------------------|
| Temperature   | \< 120°C        | \> 130°C    | \> 150°C          |
| Current       | ~28A            | \> 31A      | \> 35A            |
| Vibration     | \< 2.8 mm/s RMS | —           | (per ISO 10816-3) |

## **A.2 Water Pump — Manufacturer Specification (Dayliff) + International Standard (ISO 9906)**

Davis & Shirtliff (brand: Dayliff) is confirmed as a dominant regional pump supplier across East and Southern Africa with direct Malawi market presence. Note the difference in source tier from A.1: the figures below trace to a manufacturer datasheet, not an ISO/IEC standard document — a real, named, citable source, but not the same tier of authority. They are manufacturer-rated operating limits, not a normal/warning/critical scale, and are not yet confirmed against the specific submersible borehole model class likely to be used in a full deployment.

| **Parameter**       | **Manufacturer-Rated Limit** | **Note**                                                                                                          |
|---------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Fluid Temperature   | Max +60°C                    | Rated ceiling, per Dayliff DDP datasheet                                                                          |
| Ambient Temperature | Max +40°C                    | Rated ceiling, per Dayliff DDP datasheet                                                                          |
| Dry Running         | Not permitted                | Manufacturer explicitly names dry-running as a fault condition to be avoided; a real, citable fault mode for FR-4 |
| Performance testing | ISO 9906                     | Applicable hydraulic performance acceptance-test standard for rotodynamic pumps                                   |

## **A.3 Backup Power Supply / UPS: Team-Selected Working Values**

No manufacturer datasheet or standard has been identified for equipment-level backup power supply operating parameters. The values below are team-selected working values adopted for the simulation, pending equipment-specific validation. They do not trace to a cited source and should not be read as standards-backed limits.

Malawi's grid-instability context (ESCOM load shedding and ESCOM's 20 MW Battery Energy Storage System in Lilongwe, see Section 2.1) explains why this monitoring matters. It is grid-scale infrastructure data and is not used as a source for the equipment-level values below.

| **Parameter**     | **Normal**                                              | **Abnormal**                                                                                   |
|-------------------|---------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Temperature       | Ambient \< 25°C; internal \< 60°C                       | Internal \> 75°C                                                                               |
| Current           | Stable charging current; near-zero output on grid power | High charging current (possible short); erratic output during backup (possible inverter fault) |
| Cooling fan speed | Monitor the cooling fan, not the unit itself            | \< 1000 RPM indicates cooling failure (simulated cooling-failure condition)                    |

## **A.4 Other Team-Selected Working Values**

The figures in this section have no cited standard or manufacturer datasheet. They are adopted as working values for the simulation and are pending equipment-specific validation. They are separated from A.1 and A.2 so that the difference in source strength is visible.

### **Motor RPM threshold (team-selected)**

Normal operation: within ±2% of synchronous speed. Abnormal: below 90% of rated speed under load. No source has been identified for these values.

### **Water pump: bearing temperature, current, vibration and RPM (team-selected)**

Bearing temperature, current, vibration and RPM values below are team-selected. The fluid-temperature, ambient-temperature and dry-running limits in A.2 are manufacturer-sourced.

| **Parameter**       | **Normal**          | **Abnormal**                               | **Likely cause when abnormal**                                              |
|---------------------|---------------------|--------------------------------------------|-----------------------------------------------------------------------------|
| Bearing temperature | \< 80°C             | \> 95°C                                    | Lubrication failure (gradual rise); dry running or cavitation (sudden rise) |
| Current             | Near rated current  | High current with low flow, or low current | Blockage (high current, low flow); cavitation or airlock (low current)      |
| Vibration           | \< 3.0 mm/s RMS     | \> 5.0 mm/s RMS                            | Impeller imbalance or cavitation (high axial vibration)                     |
| RPM                 | Matches motor speed | Dropping or fluctuating                    | Belt slip (dropping); suction starvation (fluctuating)                      |

### **Motor temperature (team-selected)**

Normal: below 120°C. Warning: above 130°C. Critical: above 150°C. These are the limits used in A.1. They are team-selected and are not attributed to IEC 60034-1, because the standard sets insulation-class temperature limits rather than warning thresholds for monitoring. The earlier alternative table (100°C/120°C normal, 130°C/150°C abnormal) is superseded by these values.

# **Appendix B: Design Decisions**

This appendix records the technical choices made to satisfy the requirements in Section 3. These are design decisions, not requirements: each requirement above could, in principle, be satisfied by a different technical choice. This separation follows the Requirements-vs-Design distinction — a requirement states an outcome; a design decision names the specific technology chosen to achieve it.

| **Requirement (Section 3/4)**                     | **Design Decision**                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|---------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Equipment data source (4.2)                       | Simulink model generates simulated sensor data in place of physical sensors.                                                                                                                                                                                                                                                                                                                                                                                                        |
| Communication interface (4.4)                     | Simulated sensor data is transmitted from Simulink to the processing component via a UDP or TCP socket connection.                                                                                                                                                                                                                                                                                                                                                                  |
| Processing component                              | A Python backend (Flask) receives simulated sensor data, performs threshold screening, applies the fault-classification logic, and serves the dashboard.                                                                                                                                                                                                                                                                                                                            |
| Software interface (4.3) / data storage           | A SQLite database stores sensor readings, detected faults, and equipment information.                                                                                                                                                                                                                                                                                                                                                                                               |
| Fault classification (FR-4, FR-5)                 | Threshold screening identifies candidate abnormal conditions first. A logistic regression model, trained on Simulink-generated labeled data including simulated fault conditions, then classifies the flagged condition as normal, warning, or critical and assists with severity assignment. No trained model exists at the time of this draft. The performance targets in NFR-1 and NFR-2 apply once a model is trained and evaluated on the held-out labeled simulated test set. |
| Dashboard delivery                                | The Python backend serves the dashboard via a REST API and WebSocket connection for real-time updates; the dashboard runs as a web application accessible through the latest two major versions of Chrome, Firefox, and Edge.                                                                                                                                                                                                                                                       |
| Dashboard front end                               | The dashboard is built in React using JSX. It talks to the Flask backend over the REST API and WebSocket connection described above.                                                                                                                                                                                                                                                                                                                                                |
| Near-range / remote-range connection mode (FR-11) | Near-range and remote-range connection modes are simulated, with a manual/selectable mode switch used for the demonstration. Physical Bluetooth/Wi-Fi hardware and automatic proximity detection are outside the scope of this implementation.                                                                                                                                                                                                                                      |

Open design-stage items are listed in Appendix C. They do not affect the requirements in Section 3.

# **Appendix C: Open Items and Known Limitations**

This appendix lists what is still open, so that nothing is implied to be settled when it is not.

## **Values not backed by a cited source**

- Water pump bearing-temperature, current, vibration and RPM values (Appendix A.4): team-selected, pending equipment-specific validation.

- All backup power supply / UPS values (Appendix A.3): team-selected, pending equipment-specific validation.

- Motor temperature limits (Appendix A.1 and A.4): 120°C / 130°C / 150°C are team-selected, pending equipment-specific validation.

- Motor RPM threshold (Appendix A.4): team-selected, no source identified.

- The IEC 60034-1 and ISO 10816-3 motor current and vibration references (Appendix A.1) should be checked against the exact clauses and equipment class before any use beyond this course.

## **Design-stage items**

- Whether streaming from Simulink to the backend requires a specific real-time toolbox (Section 2.5, Appendix B). This must be confirmed before implementation begins.

## **Verification status**

- No fault-classification model has been trained yet. NFR-1 and NFR-2 state the intended metric (F1-score) and targets; no results are claimed.

- All performance results will be measured on simulated data. They do not show performance on real industrial equipment (see Section 1.2, out of scope).

- The model shall not be described as meeting NFR-1 or NFR-2 until it has actually been trained and tested on the held-out labeled simulated test set.

## **Final Implementation Check Before Submission**

- Generate enough normal and fault data to train and test the classifier.

- Keep the final test dataset separate from training data.

- Generate temperature/current faults for NFR-1 and vibration faults for NFR-2.

- Measure and record F1-score, precision and recall.

- Demonstrate the 10-second status update and the 2-second critical alert requirement.

- Demonstrate the 2-second dashboard update requirement.

- Demonstrate the ≤1% data-loss requirement during a simulated interruption.

- Demonstrate both near-range and remote-range simulated modes.

- Do not claim the model has passed NFR-1/NFR-2 until the actual test has been performed.

# **Appendix D: Verification Methods**

This section records how each Non-Functional Requirement above is intended to be evaluated. These are test methods, not requirements themselves.

- NFR-1 and NFR-2 are evaluated as F1-score on a labeled simulated test set. The test set contains normal operating records and injected fault records, each labeled by the simulation. Results are computed from true positives, false positives and false negatives and are reported as performance on the simulated test set only. They are not evidence of performance on real industrial equipment.

- PR-001: Inject a known critical fault into the simulation, record the timestamp at which the status confirms the fault and the dashboard alert timestamp, both on the synchronized clock (FR-25), and confirm the elapsed time is 2 seconds or less. Also confirm that each machine's status updates at least every 10 seconds.

- PR-002: Record the timestamp at which the processing component receives a measurement and the timestamp at which it appears on the dashboard, and confirm the difference is within 2 seconds.

- NFR-5: Record uptime of the data-logging function during the test session and confirm it is at least 95%, excluding planned restarts. NFR-6 (see Section 3.5) is evaluated by disconnecting communication, generating a known number of records, reconnecting, synchronizing, and comparing the number of records generated with the number recovered.

- NFR-7: Evaluated by injecting noise into simulated sensor data and confirming the system does not produce or act on corrupted readings.

The labeled dataset shall be divided so that records used for model training are not included in the final test set. The final held-out test set shall contain normal and injected fault records. The evaluation shall report true positives, false positives, false negatives, precision, recall and F1-score. The report shall state the actual number of test records and fault cases used. Results shall be described as performance on the simulated test set only and shall not be presented as validation of real industrial equipment.
