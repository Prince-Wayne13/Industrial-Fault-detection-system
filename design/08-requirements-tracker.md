---
title: Requirements tracker
page: 8
status: draft
srs-version: v2.0
tags: [design, page, tracker]
---

# 8. Requirements tracker

Back to [[page-map]]. Previous: [[07-demo-control-panel]].

Every requirement has its own note in the `requirements` folder. Set `status` in each note to **built**, **simulated** or **left-out**. This table fills itself from those notes. It needs the Dataview plugin (Settings, Community plugins, search "Dataview").

## How each requirement is tested

Each note has a `test` line: **inject**, **look** or **inspect**. See [[07-demo-control-panel]].

```dataview
TABLE status, test, injections
FROM #requirement
SORT file.name ASC
```

## What is still not set

```dataview
TABLE status
FROM #requirement
WHERE status = "not-set"
SORT file.name ASC
```

## Simulated

```dataview
TABLE status
FROM #requirement
WHERE status = "simulated"
SORT file.name ASC
```

## Left out

```dataview
TABLE status
FROM #requirement
WHERE status = "left-out"
SORT file.name ASC
```

## Built

```dataview
TABLE status
FROM #requirement
WHERE status = "built"
SORT file.name ASC
```
