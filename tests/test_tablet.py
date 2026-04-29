from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_tablet_viewport_loads():
    driver = get_driver(width=768, height=1024)  # iPad portrait
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        save_screenshot(driver, "tablet_homepage")
        print("✅ Homepage loaded on tablet viewport (768x1024)")
    finally:
        driver.quit()


def test_tablet_has_navigation():
    driver = get_driver(width=768, height=1024)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        nav = driver.find_elements(By.TAG_NAME, "nav")
        assert len(nav) > 0, "Navigation should be present on tablet view"
        print("✅ Navigation present on tablet")
    finally:
        driver.quit()


def test_tablet_landscape_loads():
    driver = get_driver(width=1024, height=768)  # iPad landscape
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "tablet_landscape")
        print("✅ Tablet landscape (1024x768) loaded")
    finally:
        driver.quit()


def test_tablet_collections_page():
    driver = get_driver(width=768, height=1024)
    try:
        driver.get(f"{BASE_URL}/collections/all")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "tablet_collections")
        print("✅ Collections page loaded on tablet")
    finally:
        driver.quit()
