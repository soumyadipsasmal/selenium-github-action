import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_homepage_loads_within_10_seconds():
    driver = get_driver()
    try:
        start = time.time()
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        elapsed = time.time() - start
        print(f"⏱️ Homepage load time: {elapsed:.2f}s")
        assert elapsed < 10, f"Homepage took too long to load: {elapsed:.2f}s"
        print("✅ Homepage loaded within 10 seconds")
    finally:
        driver.quit()


def test_navigation_timing_api():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        timing = driver.execute_script("""
            const t = window.performance.timing;
            return {
                dns: t.domainLookupEnd - t.domainLookupStart,
                connect: t.connectEnd - t.connectStart,
                ttfb: t.responseStart - t.requestStart,
                domLoad: t.domContentLoadedEventEnd - t.navigationStart,
                fullLoad: t.loadEventEnd - t.navigationStart,
            };
        """)
        print(f"📊 DNS: {timing['dns']}ms | Connect: {timing['connect']}ms | "
              f"TTFB: {timing['ttfb']}ms | DOM: {timing['domLoad']}ms | "
              f"Full: {timing['fullLoad']}ms")
        assert timing["domLoad"] < 15000, f"DOM load should be < 15s, was {timing['domLoad']}ms"
        print("✅ Navigation timing within acceptable limits")
    finally:
        driver.quit()


def test_collections_page_load_speed():
    driver = get_driver()
    try:
        start = time.time()
        driver.get(f"{BASE_URL}/collections/all")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        elapsed = time.time() - start
        print(f"⏱️ Collections page load time: {elapsed:.2f}s")
        assert elapsed < 12, f"Collections page too slow: {elapsed:.2f}s"
        print("✅ Collections page loaded within 12 seconds")
    finally:
        driver.quit()
