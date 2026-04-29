from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_scroll_to_bottom():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        save_screenshot(driver, "scroll_bottom")
        footer = driver.find_elements(By.TAG_NAME, "footer")
        assert len(footer) > 0, "Footer should exist after scrolling to bottom"
        print("✅ Scrolled to bottom — footer visible")
    finally:
        driver.quit()


def test_scroll_to_top():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 0);")
        scroll_y = driver.execute_script("return window.scrollY;")
        assert scroll_y == 0, "Page should scroll back to top"
        save_screenshot(driver, "scroll_top")
        print("✅ Scrolled back to top — scrollY=0")
    finally:
        driver.quit()


def test_page_height_greater_than_viewport():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_height = driver.execute_script("return document.body.scrollHeight;")
        viewport_height = driver.execute_script("return window.innerHeight;")
        print(f"ℹ️ Page height: {page_height}px | Viewport: {viewport_height}px")
        assert page_height >= viewport_height, "Page should be at least as tall as viewport"
        print("✅ Page height validated")
    finally:
        driver.quit()


def test_scroll_to_middle():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_height = driver.execute_script("return document.body.scrollHeight;")
        driver.execute_script(f"window.scrollTo(0, {page_height // 2});")
        scroll_y = driver.execute_script("return window.scrollY;")
        save_screenshot(driver, "scroll_middle")
        assert scroll_y > 0, "Page should have scrolled"
        print(f"✅ Scrolled to middle — scrollY={scroll_y}")
    finally:
        driver.quit()
