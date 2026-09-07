"""Quick full-page screenshot helper for local QA.

Not shipped — lives under tools/ next to verify_hero.py. Uses whatever
Playwright + Chromium are already on the machine.
"""
from playwright.sync_api import sync_playwright

URL = "http://localhost:8765/ltselzer-portfolio.html"
TABS = ["personal", "golf", "history", "upcoming", "swing"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    try:
        page.locator('.gate-role-btn[data-role="visitor"]').click(timeout=1500)
    except Exception:
        pass
    page.wait_for_timeout(700)
    for tab in TABS:
        # Click the matching tab button — data-tab is the stable hook.
        try:
            page.locator(f'.tab[data-tab="{tab}"]').first.click(timeout=1500)
        except Exception:
            pass
        page.wait_for_timeout(400)
        out = f"tools/_shot_{tab}.png"
        page.screenshot(path=out, full_page=True)
        print(f"wrote {out}")
    ctx.close()
    browser.close()
