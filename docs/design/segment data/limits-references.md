---
title: Limits and references
status: draft
srs-version: v2.0
tags: [design, limits, references, appendix-a]
---

# Limits and references

Back to [[page-map]]. The numbers below are the ones in `system/backend/config.py`. Change them there only.
Looked up and written on 26 October 2026. Where the SRS already gives a number, the SRS number is kept.

## How many statuses each parameter has

A parameter has three statuses (normal, warning, critical) only where there are two limits to cross. Every other parameter has two: **normal** and **abnormal** (FR-5).

| Machine | Parameter | Statuses |
| --- | --- | --- |
| Motor | Temperature | normal, warning, critical |
| Motor | Current | normal, warning, critical |
| Motor | Vibration | normal, warning, critical (new: was "per ISO 10816-3") |
| Motor | RPM | normal, abnormal |
| Pump | Bearing temperature | normal, abnormal |
| Pump | Current | normal, abnormal (too high or too low) |
| Pump | Vibration | normal, abnormal |
| Pump | RPM | normal, abnormal |
| UPS | Internal temperature | normal, abnormal |
| UPS | Current | normal, abnormal |
| UPS | Cooling fan speed | normal, abnormal |

## The limits

"Rated" values are the nameplate numbers of the simulated machines (`RATED` in config.py). They are assumptions for the simulation, so the team can change them.

| Machine | Parameter | Normal | Warning | Critical / Abnormal | Where it comes from |
| --- | --- | --- | --- | --- | --- |
| Motor | Temperature | below 120 °C | above 130 °C | above 150 °C | SRS A.1, team-selected |
| Motor | Current | about 28 A | above 31 A | above 35 A | SRS A.1. 35 A is 125% of 28 A, the usual overload ceiling [R5] |
| Motor | Vibration | below 2.8 mm/s RMS | above 2.8 | above 4.5 | **New.** ISO 10816-3 / 20816-3, Group 2, rigid support: zone B/C and C/D boundaries [R1] |
| Motor | RPM | within 2% of synchronous (1500 rpm, 4-pole, 50 Hz) [R2] | none | **abnormal below 1332 rpm** | **New number.** SRS A.4 rule: below 90% of rated speed. 0.9 x 1480 rpm |
| Pump | Bearing temperature | below 80 °C | none | abnormal above 95 °C | SRS A.4, team-selected |
| Pump | Current | near rated (12 A) | none | **abnormal above 13.8 A or below 9.6 A** | **New.** Above: 115% of rated, the overload setting for pumps [R5]. Below: 80% of rated, the usual underload / dry-running trip [R3][R4] |
| Pump | Vibration | below 3.0 mm/s RMS | none | abnormal above 5.0 | SRS A.4, team-selected |
| Pump | RPM | matches motor speed | none | **abnormal below 1305 rpm** | **New number.** Same 90% rule as the motor (0.9 x 1450 rpm) [R2] |
| UPS | Internal temperature | below 60 °C | none | abnormal above 75 °C | SRS A.3, team-selected |
| UPS | Current | rated (5 A) | none | **abnormal above 5.25 A** | **New.** 105% of rated: UPS makers start the overload timer at 105% [R6] |
| UPS | Cooling fan speed | normal | none | abnormal below 1000 rpm | SRS A.3, team-selected |

Other numbers the engine uses:

| Setting | Value | Why |
| --- | --- | --- |
| Reading | 1 per second per parameter | FR-3a |
| Window | 10 seconds | FR-6, PR-001 |
| Share of the window that must be abnormal | all of it (100%) | Decision 3, the starting rule. Change `TREND_FRACTION` |
| Sensor silent | 3 seconds | FR-13 |
| Physically possible readings | temperature -20 to 300 °C, current 0 to 500 A, vibration 0 to 50 mm/s, RPM 0 to 3600, fan RPM 0 to 10000 | Decision 2. Team-chosen, wide on purpose: they catch broken data, not faults |

## What to say about these in the SRS

- Appendix A.1: replace "(per ISO 10816-3)" with "above 4.5 mm/s RMS", add "warning above 2.8 mm/s RMS". Say the group and support used (Group 2, rigid).
- Appendix A.3 and A.4: add the pump current, pump RPM, motor RPM and UPS current numbers above. Keep them marked "team-selected, supported by [R2] to [R6]". They are still pending validation on real equipment.
- Appendix C ("Values not backed by a cited source"): the UPS current number moves out of that list only in the sense that the 105% overload start is a manufacturer practice. The rated 5 A itself is still our assumption.
- Pump vibration leaves a gap between 3.0 mm/s (normal below) and 5.0 mm/s (abnormal above). The code treats anything up to 5.0 as normal. Say so in A.4, or close the gap.
- Pump RPM "dropping or fluctuating" (A.4): only "dropping below 90%" is built. Fluctuation needs a rule such as a spread across the window. Open item.

## References

Read on 26 October 2026. Tags match the comments in `config.py`.

| Tag | Source | Used for |
| --- | --- | --- |
| SRS | Industrial Fault Detection SRS v2.0, Appendix A | Every number marked SRS |
| R1 | Fabrico, "ISO 10816-3 Vibration Severity: Zones, Limits and How to Read Them", https://www.fabrico.io/blog/iso-10816-3-vibration-severity/ and "ISO 20816 Vibration Severity Zones", https://www.fabrico.io/blog/iso-20816-vibration-severity-zones/ | Group 2 (15 to 300 kW, shaft height 160 to 315 mm), rigid support: zone boundaries 1.4, 2.8 and 4.5 mm/s RMS. ISO 10816-3 was replaced by ISO 20816-3 with the same boundaries |
| R2 | Fabrico, "Motor Slip Explained", https://www.fabrico.io/blog/motor-slip-induction/ ; WAEC Basic Electronics 2023 worked answer, https://waeconline.org.ng/e-learning/Electronics/Elect240mq3.html | A 4-pole motor on 50 Hz has synchronous speed 1500 rpm and runs a few per cent below it (1450 rpm is 3.33% slip) |
| R3 | Littelfuse, 111P / 233P Single-Phase PumpSaver datasheet, https://www.farnell.com/datasheets/3577323.pdf | Dry-well / dead-head trip adjustable from 70 to 90% of full load |
| R4 | Littelfuse, 777 electronic overload relay, https://m.littelfuse.com/products/landing-pages/electrical/demos/777-demo-1.aspx | An undercurrent setting of 80% of full-load current is usually enough |
| R5 | Industrial Monitor Direct, "Configuring Thermal Overload Relays for 3-Phase Motors", https://industrialmonitordirect.com/hu/blogs/knowledgebase/configuring-thermal-overload-relays-for-3-phase-motors-setting-calculation-and-application | NEC / NEMA: overload no more than 125% of full-load current (service factor 1.15), 115% otherwise; pumps 110 to 115% |
| R6 | City of Winnipeg, Static UPS specification, https://legacy.winnipeg.ca/finance/findata/matmgt/documents/2011/253-2011/253-2011_NMS_263353_Static_Uninterruptible_Power_Supply.pdf ; Purdi CertaUPS C650 datasheet, https://store.purdi.com/ext/pdf/datasheet.php?id=106108 ; Schneider Electric Easy UPS 3-phase specifications, https://www.productinfo.schneider-electric.com/easyups3pmodular/990-91580-technical-specifications-easy-ups-3-phase-modular/English/ | UPS overload ratings start at 105% of rated load (105 to 125% for minutes, then 125 to 150% for a minute or less, then bypass) |

### Honest limits of these references

- R1 to R6 are manufacturer, engineering-blog and specification pages. They are real and citable, but they are not the standards themselves. ISO 20816-3 and IEC 60034-1 are paid documents. If the lecturer wants the standard cited, get it from the university library and check the zone boundaries against R1.
- The ISO zone limits depend on machine size group and foundation. Group 2 and rigid support are assumed for the simulated motors. If the motors are bigger than 300 kW or on flexible mounts, use the other rows of the standard.
- The 80% and 115% pump current figures come from protection-relay practice, not from a pump standard. They are reasonable defaults, not measured limits for a particular Dayliff model.
- Nothing here has been checked on real equipment. The SRS already says so for the values it selected.
