---
title: Admin
status: draft
srs-version: v2.0
roles: [Administrator]
tags: [design, page, industrial-fault-detection]
---

# Admin

Back to [[page-map]]. Previous: [[sign-in]] (this is where the Administrator lands after signing in).

The Administrator's page. It controls who can use the system and which machines it watches. The Administrator manages the system and is not an operational user: no fault pop-ups, no fault bell list, no acknowledging ([[FR-7b]]). Supports [[UC-5]].

## Layout

```
+------------------------------------------------------------+
| Fault-Detect          (bell 1)    Name v                   |
+------------------------------------------------------------+
| [ Users ]  [ Machines ]  [ Storage ]  [ Change log ]       |
+------------------------------------------------------------+
| USERS                                      [ Add user ]    |
| Full name    | Username | Role      | Actions              |
| Mary Banda   | mbanda   | Operator  | [Edit] [Remove]      |
| John Phiri   | jphiri   | Engineer  | [Edit] [Remove]      |
+------------------------------------------------------------+
```

Four tabs on one page. No other page is needed for the Administrator. The top bar is the shared one in [[top-bar]], but its bell only ever carries the storage alert.

## Tab 1: Users

| Part | What it does | Requirement |
| --- | --- | --- |
| User list | Everyone with an account: full name, username, role. | [[UC-5]] step 2 |
| Add user | A form with full name, username, role (Operator, Engineer or Administrator) and a password. | [[UC-5]] step 2 |
| Edit user | Change the details or the role. | [[UC-5]] step 2 |
| Remove user | Removes the account. If that person appears in fault history, the records stay and nothing is silently deleted. A message says so. | [[UC-5]] step 2a |
| Password rules | At least 8 characters, and 64 or more accepted. No forced capitals, numbers or symbols. Common or leaked passwords are refused. | [[FR-28a]], [[FR-28b]], [[FR-28c]] |

## Tab 2: Machines

This is where machines are registered. It is not the [[machines-list]], which the Operator and Engineer use to look at machines.

| Part | What it does | Requirement |
| --- | --- | --- |
| Machine list | Every registered machine with its name and type (motor, water pump, backup power). | [[FR-24]] |
| Register machine | A form with a name and a type. Several machines of one type are allowed. | [[UC-5]] step 2 |
| Edit and remove | Same as users. A machine with fault history keeps its records. | [[UC-5]] step 2a |

## Tab 3: Storage

```
Storage used   [##########################-----]  72%
Alert level 75%
```

| Part | What it does | Requirement |
| --- | --- | --- |
| Storage bar | How much of the set storage is used. | [[FR-21a]] |
| Storage alert | At 75% used, an alert goes to the Administrator only. It shows on the bell and as a notice at the top of this tab. | [[FR-21a]] |

What the personnel decide after the alert (delete, update or something else) is not part of the requirements. The page only raises the alert.

## Tab 4: Change log

| Part | What it does | Requirement |
| --- | --- | --- |
| Log list | Each line says what changed, who changed it and when. It covers user changes, machine registration and limit changes. | [[FR-22]] |

A limit changed by an Engineer on [[settings]] also appears here ([[FR-22]]).

## Who can open it

| Role | Admin page |
| --- | --- |
| Administrator | yes |
| Operator | no, access is denied |
| Engineer | no, access is denied |

Anyone else who tries to open it is turned away ([[UC-5]] step 1a, [[FR-27]]).

## Use case steps

| Step in [[UC-5]] | On this page |
| --- | --- |
| 1. The administrator opens the administration area. | The page opens after [[sign-in]]. |
| 2. Adds, edits or removes a user, or registers a machine. | Tabs Users and Machines. |
| 3. The system applies it and records who and when. | The change log. |
| 1a. Someone without the role tries to open it. | Access denied. |
| 2a. Removing something with fault history. | The records are kept. |

## Open

- The Administrator cannot reset another person's password. This is decided.
- The Administrator can see the [[overview]] but gets no fault pop-ups. How the Administrator gets there from this page is not decided.
- The full name field is a new decision, see [[srs-changes]].
