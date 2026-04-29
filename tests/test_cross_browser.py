"""
Cross-browser tests using Chrome with different user-agent strings to simulate
Firefox and Edge. For true cross-browser testing, swap in webdriver.Firefox()
or webdriver.Edge() with the appropriate driver installed.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import save_screenshot, BASE_URL


def _get_driver_with_ua(user_agent: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"--user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)
    return driver


CHROME_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
FIREFOX_UA = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) "
    "Gecko/20100101 Firefox/124.0"
)
EDGE_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
)
SAFARI_MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


def test_chrome_user_agent():
    driver = _get_driver_with_ua(CHROME_UA)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        save_screenshot(driver, "crossbrowser_chrome")
        print("✅ Chrome UA — page loaded")
    finally:
        driver.quit()


def test_firefox_user_agent():
    driver = _get_driver_with_ua(FIREFOX_UA)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        save_screenshot(driver, "crossbrowser_firefox")
        print("✅ Firefox UA — page loaded")
    finally:
        driver.quit()


def test_edge_user_agent():
    driver = _get_driver_with_ua(EDGE_UA)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        save_screenshot(driver, "crossbrowser_edge")
        print("✅ Edge UA — page loaded")
    finally:
        driver.quit()


def test_safari_mobile_user_agent():
    driver = _get_driver_with_ua(SAFARI_MOBILE_UA)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        save_screenshot(driver, "crossbrowser_safari_mobile")
        print("✅ Safari Mobile UA — page loaded")
    finally:
        driver.quit()
