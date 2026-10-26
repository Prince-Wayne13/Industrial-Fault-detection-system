---
title: Top bar
status: draft
srs-version: v2.0
roles: [Operator, Engineer, Administrator]
tags: [design, shared, industrial-fault-detection]
---

# Top bar and name side bar

Back to [[page-map]].

Shown at the top of every page after [[01-sign-in]]. It is the same everywhere, so it is written once here.

## Layout

```
+--------------------------------------------------------------------+
| Fault-Detect  [ Search machines ... ]  [BT] [Wi-Fi]  (bell 3)  Name v |
+--------------------------------------------------------------------+
```

`[BT]` is the Bluetooth icon and `[Wi-Fi]` is the Wi-Fi icon. See Connection icons below.

When the name is clicked, a side bar slides in from the right:

```
                          +----------------------+
                          |  Full name           |
                          |  Role                |
                          |  Settings            |
                          +----------------------+
```

## Parts

| Part | What it does | Requirement |
| --- | --- | --- |
| Software name | Fault-Detect, on the left. Click to go home. | none |
| Search bar | Finds a machine by its name and opens it. | none |
| Bluetooth and Wi-Fi icons | Show which link the dashboard is using to reach the system. The one in use glows blue. A link that is not there is grey. Click either icon to choose a mode by hand. | [[FR-11]], [[srs-changes]], change 11 |
| Bell icon | A number on it counts faults that are acknowledged and not yet resolved. Click it to open a small window listing them. | [[srs-changes]], change 3 |
| Bell list | Each line is one fault. Choosing it opens that machine's [[04-machine-detail]]. When the Engineer resolves a fault, it leaves the list and the number goes down. | [[FR-17]] |
| Fault pop-up | Separate from the bell. See [[fault-popup]]. | [[FR-7]], [[FR-7a]], [[FR-7c]] |
| Name, top right | The signed-in person's name. Click it to open the side bar. | none |
| Side bar | Shows the full name and the role, and a Settings link that opens [[05-settings]]. | none |

## Connection icons

Two icons sit between the search bar and the bell. Bluetooth is the near-range link and Wi-Fi is the remote-range link ([[FR-11]]). Every role sees them. They are the same on every page.

### The three looks

| State | Bluetooth / Wi-Fi icon looks like | Word shown on hover and to a screen reader |
| --- | --- | --- |
| Active | Blue (`--link-active`) with a soft glow (`--link-glow`). This is the link carrying the data now. | "Bluetooth: connected" or "Wi-Fi: connected" |
| Available | Normal ink colour, no glow. The link is there but not in use. | "Bluetooth: available" or "Wi-Fi: available" |
| Offline | Grey (`--link-offline`), with a small slash across it. | "Bluetooth: offline" or "Wi-Fi: offline" |

The glow is never the only signal. The slash and the hover word say the same thing, so the meaning does not rest on colour alone (see the colour rule in [[srs-changes]]).

### Automatic mode (the default)

1. The dashboard looks for the Bluetooth of the system at work. If it finds it, it uses Bluetooth. The Bluetooth icon glows blue.
2. If that Bluetooth is not found, or is lost, the dashboard moves to Wi-Fi if Wi-Fi is available. The Wi-Fi icon glows blue and the Bluetooth icon turns grey.
3. If neither link is there, both icons are grey and the bar shows the word "Offline". The system keeps collecting and storing readings as in [[UC-4]] and [[NFR-6]].
4. While on Wi-Fi, the dashboard keeps looking for the work Bluetooth. When it is found again, the dashboard moves back to Bluetooth. Near is preferred over remote.
5. Each switch shows a short note under the icons, for example "Switched to Wi-Fi". It goes away by itself. It is not a fault pop-up and needs no acknowledging ([[fault-popup]]).

### Manual mode

Clicking either icon opens a small menu:

```
                    +----------------------+
                    | (o) Automatic        |
                    | ( ) Bluetooth only   |
                    | ( ) Wi-Fi only       |
                    +----------------------+
```

| Choice | What the dashboard does |
| --- | --- |
| Automatic | Follows the five steps above. This is the default. |
| Bluetooth only | Uses Bluetooth and nothing else. If Bluetooth is not there, its icon is grey and the bar shows "Offline". It does not fall back to Wi-Fi by itself. |
| Wi-Fi only | Uses Wi-Fi and nothing else. If Wi-Fi is not there, its icon is grey and the bar shows "Offline". It does not move to Bluetooth by itself. |

A hand choice stays until the person changes it back to Automatic. While a hand choice is on, the icon that is chosen carries a small dot so it is clear the mode is not automatic.

## Who sees what in the bell

| Role | The bell shows |
| --- | --- |
| Operator | the faults they acknowledged that are not resolved yet |
| Engineer | the faults they acknowledged that are not resolved yet |
| Administrator | no fault alerts ([[FR-7b]]); the storage alert only ([[FR-21a]]) |

## Open

- Connection icons: a browser page cannot quietly scan for Bluetooth. Web Bluetooth works only in some browsers (Chrome and Edge, not Firefox or Safari) and only after the person picks the device once. In the finished system the near link may need to go through a gateway at the work site. [[FR-11]] asks only for a simulated mode in the demonstration, so the demonstration imitates the detection with the switches on [[07-demo-control-panel]]. The team should record the real route in the design decisions.
- Connection icons: how long a link must be missing before the dashboard moves to the other one. No figure is set, so none is written here.
- Connection icons: whether the "Available" look (ink colour, no glow) is wanted, or only blue and grey.
- Connection icons: whether a hand choice is remembered for the person or for the device.
- Connection icons: whether a switch from one link to the other counts as an interruption under [[UC-4]].

- Search is set to find machines by name. Nothing in the SRS asks for search, so this is a design choice and the tracker will show it as extra.
- The SRS does not say an account has a full name. It only says the Administrator manages accounts ([[UC-5]]). If the side bar shows a full name, the SRS needs one line saying accounts hold it.
- Whether the Administrator's bell shows the storage alert as a number or only on [[06-admin]] is not decided.
