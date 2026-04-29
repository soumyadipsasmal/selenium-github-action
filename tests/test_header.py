from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_header_exists():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        header = driver.find_elements(By.TAG_NAME, "header")
        assert len(header) > 0, "Page should have a <header> element"
        print("✅ Header element found")
    finally:
        driver.quit()


def test_header_has_logo():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Logo is usually an <img> or SVG inside the header or a link with class containing 'logo'
        logos = driver.find_elements(By.XPATH,
            "//*[contains(@class,'logo') or contains(@id,'logo') or contains(@alt,'logo')]"
        )
        assert len(logos) > 0, "Header should contain a logo element"
        print(f"✅ Logo element found: {logos[0].tag_name}")
    finally:
        driver.quit()


def test_header_has_navigation():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        nav = driver.find_elements(By.TAG_NAME, "nav")
        assert len(nav) > 0, "Page should contain a <nav> element"
        print(f"✅ Navigation element found")
    finally:
        driver.quit()


def test_header_cart_icon_visible():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        cart = driver.find_elements(By.XPATH,
            "//*[contains(@href,'cart') or contains(@class,'cart') or contains(@id,'cart')]"
        )
        assert len(cart) > 0, "Header should have a cart icon/link"
        print("✅ Cart icon found in header")
        save_screenshot(driver, "header_cart")
    finally:
        driver.quit()
