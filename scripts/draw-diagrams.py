"""Draws the two SRS diagrams as SVG.

Usage: python3 draw-diagrams.py OUTPUT_DIR
Then render each .svg to .png (for example with Chromium or Inkscape) and insert the PNGs in the Word file.
Labels come straight from Section 3.2 (use cases), Section 3.1.1 (roles) and Section 4 (interfaces).
"""
import math, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
FONT = 'font-family="Arial, Helvetica, DejaVu Sans, sans-serif"'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def text(x, y, s, size=22, anchor='middle', weight='normal', style='normal', fill='#000'):
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" fill="{fill}">{esc(s)}</text>')


def lines(x, y, parts, size=22, lh=None, **kw):
    lh = lh or size * 1.3
    return ''.join(text(x, y + i * lh, p, size=size, **kw) for i, p in enumerate(parts))


def actor(x, y, label):
    """Stick figure with the head centred on (x, y)."""
    s = [f'<circle cx="{x}" cy="{y}" r="18" fill="#fff" stroke="#000" stroke-width="2.5"/>',
         f'<line x1="{x}" y1="{y+18}" x2="{x}" y2="{y+75}" stroke="#000" stroke-width="2.5"/>',
         f'<line x1="{x-32}" y1="{y+40}" x2="{x+32}" y2="{y+40}" stroke="#000" stroke-width="2.5"/>',
         f'<line x1="{x}" y1="{y+75}" x2="{x-28}" y2="{y+115}" stroke="#000" stroke-width="2.5"/>',
         f'<line x1="{x}" y1="{y+75}" x2="{x+28}" y2="{y+115}" stroke="#000" stroke-width="2.5"/>',
         text(x, y + 152, label, size=24, weight='bold')]
    return ''.join(s)


def ellipse_edge(cx, cy, rx, ry, px, py):
    dx, dy = px - cx, py - cy
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


def oval(cx, cy, parts, rx, ry):
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" stroke="#000" stroke-width="2.5"/>'
    y0 = cy - (len(parts) - 1) * 16 + 9
    for i, p in enumerate(parts):
        s += text(cx, y0 + i * 32, p, size=25)
    return s


def svg_wrap(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{esc(title)}</title><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')


# ================================================================ use-case diagram
W, H = 1250, 1160
RX, RY = 320, 54
CX = 625
b = []
b.append('<rect x="250" y="30" width="750" height="960" fill="#fff" stroke="#000" stroke-width="2.5"/>')
b.append(text(CX, 76, 'Industrial Fault Detection System', size=28, weight='bold'))
ovals = {
    'UC-2': (165, ['UC-2: Detect a Fault and', 'Alert the User']),
    'UC-3': (315, ['UC-3: Review Fault History', 'and Generate a Report']),
    'UC-1': (465, ['UC-1: Monitor', 'Equipment Status']),
    'UC-5': (615, ['UC-5: Administer Users', 'and Equipment']),
    'UC-4': (765, ['UC-4: Continue Monitoring During', 'a Connection Interruption']),
    'UC-6': (915, ['UC-6: Place Equipment in', 'Maintenance Mode']),
}
for k, (cy, parts) in ovals.items():
    b.append(oval(CX, cy, parts, RX, RY))


def inside(k, x, y):
    cy = ovals[k][0]
    return ((x - CX) / RX) ** 2 + ((y - cy) / RY) ** 2


def assoc(ax, ay, key):
    cy = ovals[key][0]
    ex, ey = ellipse_edge(CX, cy, RX, RY, ax, ay)
    for other in ovals:                       # the line must not pass through any other oval
        if other == key:
            continue
        for i in range(101):
            t = i / 100
            x, y = ax + (ex - ax) * t, ay + (ey - ay) * t
            assert inside(other, x, y) > 1.08, ('line to', key, 'crosses', other)
    return f'<line x1="{ax}" y1="{ay}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#000" stroke-width="2.2"/>'


OPX, OPY = 110, 275     # arm height 315 = UC-3
ENX, ENY = 110, 875     # arm height 915 = UC-6
ADX, ADY = 1135, 500    # arm height 540 = between UC-1 and UC-5
b.append(actor(OPX, OPY, 'Operator'))
b.append(actor(ENX, ENY, 'Engineer'))
b.append(actor(ADX, ADY, 'Administrator'))
for k in ('UC-2', 'UC-3', 'UC-1'):
    b.append(assoc(OPX + 32, OPY + 40, k))
b.append(assoc(ENX + 32, ENY + 40, 'UC-6'))
for k in ('UC-1', 'UC-5'):
    b.append(assoc(ADX - 32, ADY + 40, k))
# generalisation: the Engineer inherits the Operator (hollow triangle on the Operator end)
gt = OPY + 152 + 12
b.append(f'<line x1="{OPX}" y1="{ENY-18}" x2="{OPX}" y2="{gt+24}" stroke="#000" stroke-width="2.2"/>')
b.append(f'<polygon points="{OPX},{gt} {OPX-13},{gt+24} {OPX+13},{gt+24}" fill="#fff" stroke="#000" stroke-width="2.2"/>')
b.append(text(30, 1100, 'Solid line: the user takes part in the use case. Hollow arrow: the Engineer has every right the Operator has.', size=20, anchor='start', fill='#222'))
b.append(text(30, 1130, 'UC-2 and UC-4 start automatically. UC-2 alerts the Operator or Engineer. UC-4 involves no user action.', size=20, anchor='start', fill='#222'))
open(os.path.join(OUT, 'use-case-diagram.svg'), 'w').write(svg_wrap(W, H, ''.join(b), 'Use-case diagram'))

# ================================================================ context diagram
W2, H2 = 1400, 1010
c = []
c.append('<defs><marker id="ah" markerUnits="userSpaceOnUse" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="15" markerHeight="15" orient="auto">'
         '<path d="M0,0 L12,6 L0,12 z" fill="#000"/></marker></defs>')
c.append('<rect x="470" y="40" width="320" height="920" rx="14" fill="#fff" stroke="#000" stroke-width="3"/>')
c.append(lines(630, 480, ['Industrial Fault', 'Detection System'], size=30, lh=40, weight='bold'))
c.append('<rect x="10" y="440" width="240" height="120" fill="#fff" stroke="#000" stroke-width="2.5"/>')
c.append(lines(130, 490, ['Equipment data', 'source (simulated)'], size=22, lh=30, weight='bold'))


def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="2.4" marker-end="url(#ah)"/>'


c.append(arrow(250, 500, 468, 500))
c.append(lines(360, 440, ['Sensor readings,', 'one per second', 'per parameter'], size=20, lh=25, style='italic'))
rows = [
    ('Operator', 200,
     ['Status, readings, fault', 'history, reports and', 'fault pop-ups'],
     ['Login, acknowledge a', 'fault, report requests']),
    ('Engineer', 500,
     ['Status, readings, fault', 'history, reports and', 'fault pop-ups'],
     ['Login, acknowledge or', 'resolve a fault, maintenance', 'mode, limit changes,', 'report requests']),
    ('Administrator', 800,
     ['Status, readings, fault', 'history and the 75%', 'storage alert'],
     ['Login, user accounts,', 'equipment registration', 'and settings']),
]
for name, y0, out_lbl, in_lbl in rows:
    c.append(f'<rect x="1130" y="{y0-45}" width="260" height="90" fill="#fff" stroke="#000" stroke-width="2.5"/>')
    c.append(text(1260, y0 + 9, name, size=26, weight='bold'))
    ya, yb = y0 - 22, y0 + 22
    c.append(arrow(790, ya, 1128, ya))
    c.append(lines(960, ya - 12 - 25 * (len(out_lbl) - 1), out_lbl, size=20, lh=25, style='italic'))
    c.append(arrow(1130, yb, 792, yb))
    c.append(lines(960, yb + 28, in_lbl, size=20, lh=25, style='italic'))
c.append(text(10, 995, 'Arrows show what passes between the system and the people and equipment around it.', size=19, anchor='start', fill='#222'))
open(os.path.join(OUT, 'context-diagram.svg'), 'w').write(svg_wrap(W2, H2, ''.join(c), 'Context diagram'))
print('written')
