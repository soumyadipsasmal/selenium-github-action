"""
helpers.py
──────────
General-purpose helpers for the Selenium test suite.

Usage:
    from utils.helpers import (
        wait_for_url_contains,
        wait_for_text_in_body,
        scroll_to_element,
        is_element_visible,
        get_all_hrefs,
        check_links_status,
        get_page_performance,
    )
"""

import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ── Wait helpers ──────────────────────────────────────────────────────────

def wait_for_url_contains(driver, fragment: str, timeout: int = 15) -> bool:
    """Wait until the current URL contains `fragment`. Returns True/False."""
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(fragment))
        return True
    except TimeoutException:
        return False


def wait_for_text_in_body(driver, text: str, timeout: int = 15) -> bool:
    """Wait until `text` appears anywhere in <body>. Returns True/False."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
        )
        return True
    except TimeoutException:
        return False


def wait_for_element(driver, locator: tuple, timeout: int = 15):
    """Wait for an element to be visible and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_for_element_clickable(driver, locator: tuple, timeout: int = 15):
    """Wait for an element to be clickable and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


# ── Scroll helpers ────────────────────────────────────────────────────────

def scroll_to_element(driver, element):
    """Scroll an element into the viewport using JS."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.3)


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")


def get_scroll_position(driver) -> int:
    return driver.execute_script("return window.scrollY;")


def get_page_height(driver) -> int:
    return driver.execute_script("return document.body.scrollHeight;")


# ── Element helpers ───────────────────────────────────────────────────────

def is_element_visible(driver, locator: tuple, timeout: int = 5) -> bool:
    """Return True if the element is visible within `timeout` seconds."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def is_element_present(driver, locator: tuple) -> bool:
    return len(driver.find_elements(*locator)) > 0


def safe_click(driver, locator: tuple, timeout: int = 10):
    """Scroll to element, then click it."""
    el = wait_for_element_clickable(driver, locator, timeout)
    scroll_to_element(driver, el)
    el.click()


# ── Link / HTTP helpers ───────────────────────────────────────────────────

def get_all_hrefs(driver, domain_filter: str = "") -> list[str]:
    """
    Return all href values from <a> tags on the current page.
    Pass `domain_filter` (e.g. 'anvicouture.com') to limit to internal links.
    """
    links = [
        a.get_attribute("href")
        for a in driver.find_elements(By.TAG_NAME, "a")
        if a.get_attribute("href")
    ]
    if domain_filter:
        links = [l for l in links if domain_filter in l]
    return list(set(links))


def check_links_status(urls: list[str], timeout: int = 10) -> dict:
    """
    HEAD-request each URL and return a dict:
        { url: status_code }   — status_code = -1 on connection error
    """
    results = {}
    for url in urls:
        try:
            r = requests.head(url, timeout=timeout, allow_redirects=True)
            results[url] = r.status_code
        except Exception:
            results[url] = -1
    return results


def get_broken_links(urls: list[str]) -> list[str]:
    """Return only the URLs that returned 4xx/5xx or failed to connect."""
    statuses = check_links_status(urls)
    return [url for url, code in statuses.items() if code < 0 or code >= 400]


# ── Performance helpers ───────────────────────────────────────────────────

def get_page_performance(driver) -> dict:
    """
    Return key timings (ms) from the browser Navigation Timing API:
        dns, connect, ttfb, dom_load, full_load
    """
    return driver.execute_script("""
        const t = window.performance.timing;
        return {
            dns:       t.domainLookupEnd  - t.domainLookupStart,
            connect:   t.connectEnd       - t.connectStart,
            ttfb:      t.responseStart    - t.requestStart,
            dom_load:  t.domContentLoadedEventEnd - t.navigationStart,
            full_load: t.loadEventEnd     - t.navigationStart,
        };
    """)


def get_browser_console_errors(driver) -> list[str]:
    """Return SEVERE browser console log messages."""
    try:
        logs = driver.get_log("browser")
        return [e["message"] for e in logs if e.get("level") == "SEVERE"]
    except Exception:
        return []


# ── Misc ──────────────────────────────────────────────────────────────────

def retry(func, retries: int = 3, delay: float = 2.0):
    """
    Retry a callable up to `retries` times on any exception.
    Returns the function's return value, or raises the last exception.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as exc:
            last_exc = exc
            print(f"  ⚠️ Attempt {attempt}/{retries} failed: {exc}")
            time.sleep(delay)
    raise last_exc
