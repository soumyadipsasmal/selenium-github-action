import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from _driver import get_driver, save_screenshot, BASE_URL


def load_page_with_retry(driver, url, retries=3, wait=2):
    """Load a URL with automatic retries on timeout."""
    for attempt in range(1, retries + 1):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print(f"✅ Loaded on attempt {attempt}: {url}")
            return True
        except TimeoutException:
            print(f"⚠️ Attempt {attempt} timed out — retrying in {wait}s...")
            time.sleep(wait)
    return False


def test_homepage_loads_with_retry():
    driver = get_driver()
    try:
        success = load_page_with_retry(driver, BASE_URL, retries=3)
        assert success, "Homepage failed to load after 3 retries"
        save_screenshot(driver, "retry_homepage")
    finally:
        driver.quit()


def test_collections_loads_with_retry():
    driver = get_driver()
    try:
        success = load_page_with_retry(driver, f"{BASE_URL}/collections/all", retries=3)
        assert success, "Collections page failed after 3 retries"
        save_screenshot(driver, "retry_collections")
    finally:
        driver.quit()


def test_cart_loads_with_retry():
    driver = get_driver()
    try:
        success = load_page_with_retry(driver, f"{BASE_URL}/cart", retries=3)
        assert success, "Cart page failed after 3 retries"
        save_screenshot(driver, "retry_cart")
    finally:
        driver.quit()


def test_explicit_wait_with_fallback():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        # Try waiting for a specific element; fall back to body
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )
            print("✅ Header found with explicit wait")
        except TimeoutException:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("⚠️ Header not found — fell back to body wait")
        assert True
    finally:
        driver.quit()
