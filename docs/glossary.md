# Glossary

Plain meanings of the terms we use. Several of these are not yet defined in Section 1.3 of the SRS and should be added.

| Term | Meaning |
| --- | --- |
| Parameter | One thing measured on a machine, such as temperature, current or vibration. |
| Reading | One value from one sensor. One reading is taken per second for every parameter on every machine. |
| Sanity check | The first check on each incoming reading. It looks for a wrong type, a missing value, or a value that is physically impossible. Failed readings are recorded as invalid and kept away from the status model (FR-14). |
| Window | A block of 10 seconds of clean readings. |
| Status model | The part that looks at one window and decides whether it is normal, warning or critical. See open item O-5 about how it relates to the classifier in Appendix B. |
| Status | The result for one window, with its time stamp. |
| Trend check | The rule that one abnormal reading is not a fault. The condition must hold across the window first (FR-6). |
| Fault bundle | The readings of a warning or critical window kept together with its status. |
| Limit | A boundary value for a parameter on one machine. New machines use the defaults for their type; Engineers can tune each machine independently. Also called a threshold. |
| Sensor fault | A parameter has stopped reporting for longer than three times its normal reporting interval (FR-13). |
| Acknowledge | A user records that they have seen an alert. The log shows who and when (FR-8). |
| Resolved | A fault has been dealt with. Recorded with the time (FR-17). |
| Maintenance mode | Equipment is being worked on for a stated time. Readings and new alerts are paused (FR-18, FR-19). |
| Connected user | Someone using the dashboard right now, near-range or remote. Alerts reach only connected users. |
| Administrator | Manages the system (accounts, equipment, settings). Not an operational user. Gets no fault alerts. Does get the storage alert. |
| Engineer | A technical user who may change limits. Every change is logged. |
| Storage alert | The alert at 75% of the set storage used. It goes to everyone connected, especially the Administrator. |

For Fault, Warning and Critical, see Section 1.3 of the SRS.
