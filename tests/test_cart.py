from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

CART_URL = f"{BASE_URL}/cart"


def test_cart_page_loads():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "cart_page")
        print(f"✅ Cart page loaded: {driver.title}")
    finally:
        driver.quit()


def test_empty_cart_message():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(kw in body_text for kw in
                   ["empty", "no item", "your cart", "cart is"]), \
            "Empty cart page should show a relevant message"
        print("✅ Empty cart message shown")
    finally:
        driver.quit()


def test_cart_has_continue_shopping_link():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        links = driver.find_elements(By.XPATH,
            "//a[contains(text(),'Continue') or contains(text(),'Shop') or "
            "contains(@href,'collection') or contains(@href,'all')]"
        )
        assert len(links) > 0, "Cart page should have a continue shopping link"
        print(f"✅ Continue shopping link: '{links[0].text}'")
    finally:
        driver.quit()


def test_cart_page_title_contains_cart():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        title_or_heading = (driver.title + driver.find_element(By.TAG_NAME, "body").text).lower()
        assert "cart" in title_or_heading
        print("✅ Cart keyword present in page")
    finally:
        driver.quit()


def test_cart_json_endpoint():
    """Shopify exposes /cart.json — validate it returns JSON data."""
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/cart.json")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "item_count" in body_text or "items" in body_text, \
            "/cart.json should return cart JSON with item_count"
        print(f"✅ /cart.json response: {body_text[:80]}")
    finally:
        driver.quit()
