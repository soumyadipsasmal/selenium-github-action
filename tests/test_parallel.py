"""
Parallel-safe tests — each test is fully self-contained with its own driver.
Run in parallel with: pytest tests/test_parallel.py -n auto  (requires pytest-xdist)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_parallel_homepage():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        print("✅ [parallel] Homepage loaded")
    finally:
        driver.quit()


def test_parallel_collections():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/collections/all")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print("✅ [parallel] Collections loaded")
    finally:
        driver.quit()


def test_parallel_cart():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/cart")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print("✅ [parallel] Cart loaded")
    finally:
        driver.quit()


def test_parallel_search():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/search?q=dress")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print("✅ [parallel] Search loaded")
    finally:
        driver.quit()


def test_parallel_login_page():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/account/login")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print("✅ [parallel] Login page loaded")
    finally:
        driver.quit()
