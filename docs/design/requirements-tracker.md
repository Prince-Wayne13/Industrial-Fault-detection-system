---
title: Requirements tracker
status: draft
srs-version: v2.0
tags: [design, page, tracker]
---

# Requirements tracker

Back to [[page-map]].

Every requirement has its own note in the `requirements` folder. Set `status` in each note to **built**, **simulated** or **left-out**. This table fills itself from those notes. It needs the Dataview plugin (Settings, Community plugins, search "Dataview").

## How each one is tested

The full table is in [[test-plan]].

```dataview
TABLE test AS "Method", scenarios AS "Scenario", status
FROM #requirement
WHERE test
SORT test ASC
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
