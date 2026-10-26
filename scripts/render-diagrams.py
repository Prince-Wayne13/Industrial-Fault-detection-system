"""Renders docs/diagrams/*.svg to .png with Chromium (Playwright). Usage: python3 scripts/render-diagrams.py docs/diagrams"""
import sys, os
from playwright.sync_api import sync_playwright
d=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(w,h) in {'use-case-diagram':(1250,1160),'context-diagram':(1400,1010)}.items():
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
        pg.goto('file://'+os.path.abspath(os.path.join(d,name+'.svg')))
        pg.screenshot(path=os.path.join(d,name+'.png'),clip={'x':0,'y':0,'width':w,'height':h})
    b.close()
print('png ok')
