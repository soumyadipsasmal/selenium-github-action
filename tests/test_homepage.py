from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_homepage_loads():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://anvicouture.com")
        print(f"✅ Homepage loaded | title: '{driver.title}'")
        save_screenshot(driver, "homepage_loaded")
    finally:
        driver.quit()


def test_homepage_title_not_empty():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.title != "", "Page title should not be empty"
        print(f"✅ Title: '{driver.title}'")
    finally:
        driver.quit()


def test_homepage_has_images():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        assert len(images) > 0, "Homepage should contain at least one image"
        print(f"✅ Found {len(images)} images on homepage")
    finally:
        driver.quit()


def test_homepage_has_links():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        links = driver.find_elements(By.TAG_NAME, "a")
        assert len(links) > 0, "Homepage should contain navigation links"
        print(f"✅ Found {len(links)} links on homepage")
    finally:
        driver.quit()


def test_homepage_url_is_https():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://"), "Site should use HTTPS"
        print("✅ Site uses HTTPS")
    finally:
        driver.quit()
