---
title: Test plan
status: draft
tags: [design, test-plan]
---

# Test plan

Back to [[page-map]].

Every requirement, how it is tested, and which seeded scenario shows it. Made by the script from `test-plan.json`. Edit that file, not this note.

## The four ways to test

| Method | Meaning |
| --- | --- |
| inject | Play a seeded scenario and watch the result. |
| look | Check something on screen. |
| inspect | Show it in the settings, the database or the code. |
| measure | Run the seed data and read off a number. |

## Every requirement

| Requirement | Method | Scenario | Passes if |
| --- | --- | --- | --- |
| [[FR-1]] | look | Normal running | Temperature, current, vibration and RPM are all shown. |
| [[FR-2]] | look | Normal running | Bearing temperature, current, vibration and RPM are all shown. |
| [[FR-3]] | look | Normal running | Internal temperature, current and fan speed are all shown. |
| [[FR-3a]] | measure | Normal running | About 60 readings, one each second, for every parameter. |
| [[FR-4]] | inject | Sustained warning | The high temperature is flagged for Motor 1. |
| [[FR-5]] | inject | Sustained warning, Sustained critical | The status shows warning, then critical, naming the machine and parameter. |
| [[FR-6]] | inject | Lone spike | No fault is raised from one reading. A fault only appears when it lasts across the 10-second check. |
| [[FR-7]] | inject | Sustained warning | A pop-up appears on both screens. |
| [[FR-7a]] | look | Sustained warning | It shows the machine, parameter, fault type, level and time. |
| [[FR-7b]] | look | Sustained warning | No pop-up and no fault bell list. |
| [[FR-7c]] | inject | Nobody connected | The fault is still open and its pop-up appears. |
| [[FR-8]] | inject | Sustained warning | The pop-up goes away for that person. |
| [[FR-8a]] | look | Sustained warning | It shows who acknowledged and when. |
| [[FR-8b]] | look | Sustained warning | It is still open, not resolved. |
| [[FR-9]] | look | Sustained warning | The fault and the readings can be called up. |
| [[FR-9a]] | inspect | Normal running | One status with a time for every 10 seconds. |
| [[FR-9b]] | inspect | Old data | Readings of old normal windows are gone. Readings of old warning or critical windows are still there with their status. |
| [[FR-10]] | look | Sustained warning | Everyone can view history. Operator and Engineer can make a report showing performance and repeated faults. |
| [[FR-11]] | inject | Near and remote mode | The dashboard shows the same equipment data in both modes. |
| [[FR-12]] | inject | Connection cut | The dashboard keeps showing local data. After restoring, the stored readings arrive. |
| [[FR-13]] | inject | Sensor goes silent | Within 3 seconds it shows a sensor fault, not the last number. |
| [[FR-14]] | inject | Bad reading | Each one is kept out, logged as invalid, and the system carries on. |
| [[FR-15]] | inject | Two faults at once | Two separate fault records appear, one for each parameter. |
| [[FR-16]] | inject | Fault returns | No second alert while it is open. A new alert only after it cleared and came back. |
| [[FR-17]] | inject | Sustained warning | The Engineer can, and the time is recorded. The Operator cannot. |
| [[FR-18]] | inject | Maintenance | Readings keep recording. New fault alerts for that machine pause. |
| [[FR-19]] | inject | Maintenance | The machine shows an overdue mark. |
| [[FR-20]] | inject | Storage fails | New readings are kept in temporary storage, the system keeps running, and the event is logged. |
| [[FR-21]] | inject | Restart | It carries on with the last settings, and machines show their status again once new readings arrive. |
| [[FR-21a]] | inject | Storage fills up | An alert goes to the Administrator only. |
| [[FR-22]] | look | Limit change | Each change is listed with who and when. |
| [[FR-23]] | inject | Limit change | The old value and the date of change are still shown. |
| [[FR-23a]] | inject | Limit change | It works with no restart. |
| [[FR-23b]] | inject | Limit change | The change is refused. |
| [[FR-23c]] | inject | Limit change | New readings use the new limit. Earlier readings are unchanged. |
| [[FR-23d]] | inject | Limit change | The fault shows the limit that was in force when it was raised. |
| [[FR-24]] | look | Normal running | Several motors appear as separate units, each with its own status and fault history. |
| [[FR-25]] | inspect | Normal running | They agree. |
| [[FR-26]] | look | Login checks | The person is signed out and must sign in again. 1 minute and 5 minutes are accepted, 6 is not. |
| [[FR-27]] | look | Login checks | Access is denied. |
| [[FR-28]] | look | Login checks | The sign-in page appears instead. |
| [[FR-28a]] | look | Login checks | 14 is refused. 15 and 64 are accepted. |
| [[FR-28b]] | look | Login checks | It is accepted, and nothing forces a change later. |
| [[FR-28c]] | look | Login checks | It is refused. |
| [[FR-28d]] | look | Login checks | The account is blocked for 15 minutes and the message says so. |
| [[FR-28e]] | inspect | Login checks | It uses https with TLS 1.2 or newer. |
| [[FR-28f]] | inspect | Login checks | It is scrambled and cannot be read back. |
| [[NFR-1]] | measure | Labelled test set | At least 95% found. |
| [[NFR-2]] | measure | Labelled test set | At least 85% found. |
| [[NFR-5]] | measure | Normal running | Data logging was running at least 95% of the time. |
| [[NFR-6]] | measure | Connection cut | At least 99% stored. |
| [[NFR-7]] | inject | Noisy readings | Valid readings stay valid. Readings that cannot be checked are thrown away, not acted on. |
| [[NFR-8]] | look | Normal running | Every machine's status is visible without opening a second window. |
| [[NFR-9]] | inspect | Normal running | Only that part changes. Nothing unrelated needs editing. |
| [[NFR-10]] | inspect | Storage fills up | Nothing is deleted automatically before 75% is reached. Normal readings still go after 24 hours. |
| [[PR-001]] | measure | Normal running | No more than 10 seconds. |
| [[PR-001a]] | measure | Sustained critical | No more than 2 seconds. |
| [[PR-001b]] | inject | Slow alert | The alert still shows, the delay is logged, and an Alerts delayed notice appears. |
| [[PR-002]] | measure | Normal running | Within 2 seconds. |
| [[PR-003]] | measure | Heavy load | Status and reading times stay within their limits. |
| [[PR-004]] | measure | Heavy load | Status and reading times stay within their limits. |
| [[PR-005]] | measure | Heavy load | At least 40 per second. |
| [[PR-006]] | inspect | Storage fills up | Room for at least 3,456,000 readings plus statuses and faults. |
| [[PR-007]] | measure | Restart | No more than 60 seconds. |

## The seeded scenarios

| Scenario | What the seed data does | Tests |
| --- | --- | --- |
| Normal running | All machines run normally for a few minutes. | 12 |
| Lone spike | One reading is far too high, then readings go back to normal. | 1 |
| Sustained warning | Motor 1 temperature stays above its warning limit for more than 10 seconds. | 11 |
| Sustained critical | A reading stays above its critical limit for more than 10 seconds. | 2 |
| Two faults at once | Motor 2 temperature and current both go abnormal together. | 1 |
| Sensor goes silent | One parameter stops sending readings. | 1 |
| Bad reading | A reading arrives as text, or empty, or impossible (for example 9999 degrees). | 1 |
| Connection cut | The link between the parts is cut for a while, then restored. | 2 |
| Storage fills up | Used storage climbs to 75%. | 3 |
| Storage fails | The main store becomes unavailable or full. | 1 |
| Restart | The system is stopped and started again. | 2 |
| Maintenance | An Engineer puts a machine into maintenance for a short time and lets it run past the time. | 2 |
| Fault returns | A fault stays open, then clears, then comes back. | 1 |
| Limit change | An Engineer changes limits, including one that is not allowed. | 6 |
| Nobody connected | A fault happens while no Operator or Engineer is signed in. | 1 |
| Noisy readings | Readings are full of noise and some are damaged. | 1 |
| Heavy load | 10 machines and 5 users at the same time. | 3 |
| Slow alert | An alert is made to arrive more than 2 seconds late. | 1 |
| Labelled test set | A set of readings where the right answer is known, to count how many faults are found. | 2 |
| Login checks | Wrong passwords, short passwords, common passwords and a user without permission. | 9 |
| Near and remote mode | Switch between the near-range and remote-range modes. | 1 |
| Old data | Readings older than 24 hours, some from normal windows and some from fault windows. | 1 |
