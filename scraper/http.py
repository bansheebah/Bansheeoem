from __future__ import annotations

import requests

from config import REQUEST_TIMEOUT_SECONDS, USER_AGENT


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    response.raise_for_status()
    return response.text


def fetch_html_browser(url: str) -> str:
    """Use only when the normal HTML response contains no part table."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install Playwright first: pip install playwright && python -m playwright install chromium") from exc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(url, wait_until="networkidle", timeout=REQUEST_TIMEOUT_SECONDS * 2)
        page.wait_for_timeout(750)
        html = page.content()
        browser.close()
    return html

