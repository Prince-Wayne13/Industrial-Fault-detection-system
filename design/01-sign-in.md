---
title: Sign in
page: 1
status: draft
srs-version: v2.0
roles: [Operator, Engineer, Administrator]
tags: [design, page, industrial-fault-detection]
---

# 1. Sign in

Back to [[page-map]]. Next: [[02-overview]].

The first screen anyone sees. Simple on purpose: the software name, two boxes and one button. The software is called **Fault-Detect**.

## Layout

```
+--------------------------------------+
|                                      |
|            Fault-Detect              |
|                                      |
|   Username                           |
|   [______________________________]   |
|                                      |
|   Password                           |
|   [______________________________]   |
|                                      |
|   [           Sign in            ]   |
|                                      |
|   (message area)                     |
|                                      |
+--------------------------------------+
```

- Centred on the page, one narrow box.
- No sign-up link. The Administrator creates accounts ([[UC-5]]).
- No menu and no other page is reachable from here. Nothing else opens before sign-in ([[FR-28]]).

## Parts of the page

| Part | What it does | Requirement |
| --- | --- | --- |
| Name "Fault-Detect" | Shows the software name at the top. | none |
| Username box | The person types their username. | [[FR-28]] |
| Password box | Hides what is typed. Accepts long passwords, 64 characters or more. | [[FR-28a]] |
| Sign in button | Checks the details. | [[FR-28]] |
| Message area | Shows the messages in the next table. | [[FR-26]], [[FR-28d]] |

## Messages

| When | What the person sees | Requirement |
| --- | --- | --- |
| Wrong details | "Username or password is not correct." | [[FR-28]] |
| 5 wrong attempts on one account | "Too many attempts. Try again in 15 minutes." | [[FR-28d]] |
| Signed out after idle time | "You were signed out because you were idle." | [[FR-26]] |

## Where the person goes after signing in

| Role | Goes to |
| --- | --- |
| Operator | [[02-overview]] |
| Engineer | [[02-overview]] |
| Administrator | [[06-admin]] |

## Rules that work behind the page

The screen does not show these, but the tracker still lists them:

- All traffic uses a secure connection ([[FR-28e]]).
- Passwords are stored scrambled, so nobody can read them back ([[FR-28f]]).
- No rule forces capital letters, numbers or symbols, and no forced password changes ([[FR-28b]]).
- Common or leaked passwords are refused. This applies when a password is set, so it belongs on [[06-admin]], not here ([[FR-28c]]).

## Use case

No use case in the SRS is only about signing in. This page supports every use case, because each one starts with "the user is logged in".

## Open

- The idle time can be 1 to 5 minutes and each user sets their own ([[FR-26]]). Where a user sets it is not decided. It is not on this page.
