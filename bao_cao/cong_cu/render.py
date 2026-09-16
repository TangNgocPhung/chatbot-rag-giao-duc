"""Render an HTML/SVG file (or inline HTML string) to PNG with headless Chromium."""
import pathlib, sys
from playwright.sync_api import sync_playwright

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

def render_many(jobs, scale=2):
    """jobs: list of (html_string, out_png, width, height_or_None)."""
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--force-color-profile=srgb'])
        for html, out, w, h in jobs:
            pg = b.new_page(viewport={'width': w, 'height': h or 800}, device_scale_factor=scale)
            pg.set_content(html, wait_until='networkidle')
            el = pg.query_selector('#fig') or pg.query_selector('svg') or pg.query_selector('body')
            el.screenshot(path=out)
            pg.close()
            print('wrote', out)
        b.close()
