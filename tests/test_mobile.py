from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_mobile_viewport_loads():
    driver = get_driver(width=390, height=844)  # iPhone 14 size
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url.startswith("https://")
        save_screenshot(driver, "mobile_homepage")
        print("✅ Homepage loaded on mobile viewport (390x844)")
    finally:
        driver.quit()


def test_mobile_has_body_content():
    driver = get_driver(width=390, height=844)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0, "Body content should not be empty on mobile"
        print(f"✅ Mobile body has {len(body_text)} characters")
    finally:
        driver.quit()


def test_mobile_viewport_width():
    driver = get_driver(width=390, height=844)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        vp_width = driver.execute_script("return window.innerWidth;")
        print(f"ℹ️ Mobile viewport width: {vp_width}px")
        assert vp_width <= 420, f"Viewport width should be mobile-sized, got {vp_width}"
        print("✅ Mobile viewport width confirmed")
    finally:
        driver.quit()


def test_mobile_images_visible():
    driver = get_driver(width=390, height=844)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        assert len(images) > 0, "Mobile view should still show images"
        save_screenshot(driver, "mobile_images")
        print(f"✅ {len(images)} images visible on mobile")
    finally:
        driver.quit()


def test_mobile_cart_link_accessible():
    driver = get_driver(width=390, height=844)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        cart_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'cart') or contains(@class,'cart')]"
        )
        assert len(cart_links) > 0, "Cart link should be accessible on mobile"
        print(f"✅ Cart link accessible on mobile viewport")
    finally:
        driver.quit()
