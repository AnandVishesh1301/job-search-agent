import contextlib
import httpx
from playwright.sync_api import sync_playwright

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
}

def fetch_with_requests(url: str, timeout: float = 20.0) -> tuple[str, str]:
    """Return (final_url, html) using requests-like client."""
    with httpx.Client(follow_redirects=True, headers=DEFAULT_HEADERS, timeout=timeout) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return (str(resp.url), resp.text)

def fetch_with_playwright(url: str, timeout_ms: int = 25000) -> tuple[str, str]:
    """Return (final_url, html) rendered by Chromium."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=DEFAULT_HEADERS["User-Agent"])
        page = context.new_page()
        page.goto(url, timeout=timeout_ms, wait_until="load")
        # Try to wait a bit for client-side rendering if any:
        with contextlib.suppress(Exception):
            page.wait_for_load_state("networkidle", timeout=5000)
        html = page.content()
        final_url = page.url
        browser.close()
        return (final_url, html)

def get_page(url: str) -> tuple[str, str]:
    """
    Strategy:
    1) requests (fast, works for most ATS)
    2) fallback to Playwright for JS-heavy pages
    """
    try:
        return fetch_with_requests(url)
    except Exception:
        return fetch_with_playwright(url)
