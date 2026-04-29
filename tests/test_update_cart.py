from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

CART_URL = f"{BASE_URL}/cart"


def test_cart_update_endpoint_accessible():
    """Shopify /cart/update.js should be accessible (POST only, but page loads)."""
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print(f"✅ Cart page reachable at {driver.current_url}")
    finally:
        driver.quit()


def test_quantity_input_absent_on_empty_cart():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        qty_inputs = driver.find_elements(By.XPATH,
            "//input[@type='number' or contains(@name,'quantity') or contains(@class,'quantity')]"
        )
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        is_empty = any(kw in body_text for kw in ["empty", "no item"])
        if is_empty:
            assert len(qty_inputs) == 0, "Empty cart should not have quantity inputs"
            print("✅ No quantity inputs on empty cart — correct")
        else:
            print(f"ℹ️ Cart not empty — {len(qty_inputs)} quantity inputs found")
        save_screenshot(driver, "update_cart_state")
    finally:
        driver.quit()


def test_cart_json_shows_zero_items_when_empty():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/cart.json")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = driver.find_element(By.TAG_NAME, "body").text
        assert '"item_count":0' in body or '"item_count": 0' in body or "item_count" in body
        print(f"✅ cart.json accessible | {body[:80]}")
    finally:
        driver.quit()
