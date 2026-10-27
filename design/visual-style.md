---
title: Visual style
status: draft
srs-version: v2.0
tags: [design, style]
---

# Visual style

Back to [[page-map]]. How every screen looks. The colours are in [[srs-changes]] (and `palette.css`). The sizes and shapes below were set in `polish.css`, which loads after the first theme and overrides it. Remove its import to get the first look back.

## The look in one line

Compact, rounded and calm: small type, cards with big rounded corners and soft shadows, pill-shaped buttons, a dark side menu.

## Sizes and shapes

| Thing | Value | Before |
| --- | --- | --- |
| Font | Inter, then the system font | system font |
| Base text | 14 px | 16 px |
| Page title | 24 px, bold | 30 px |
| Section heading | 16 px | 20 px |
| Card corners | 20 px | 14 px |
| Control corners | 12 px (inputs, icon buttons, nav items) | 10 px |
| Buttons and status pills | fully rounded, 38 px high | 44 px, square-ish |
| Card padding | 14 to 16 px | 18 to 22 px |
| Card shadow | two soft layers, very light | one stronger layer |
| Side menu | 232 px wide, items 40 px high | 248 px, 46 px |
| Top bar | 60 px high, flat, with a thin line below | 68 px with a shadow |
| Summary tiles | small label in capitals above a 26 px number | 36 px number |
| Machine status | a thin coloured line along the top of the card | a thick line on the left |

## Colours changed by `polish.css`

| Token | Value |
| --- | --- |
| `--bg-canvas` | `#eef1f5` |
| `--bg-card` | `#ffffff` |
| `--bg-sidebar` | `#1f2d3d` |
| `--border-light` | `#e3e8ee` |
| `--text-head` | `#1b2634` |
| `--text-body` | `#526071` |

The status colours (teal, warning, red, purple) and the connection icon colours are unchanged. Status is still shown as a word as well as a colour.

## Rules

- Cards hold one idea each: a machine, a reading, a window, a table.
- Fault pop-ups are narrower (360 px) and show one at a time. See [[fault-popup]].
- Empty limit boxes on [[05-settings]] have a dashed border and say "not necessary".
- The dark theme is still not designed. See [[srs-changes]].
