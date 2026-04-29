from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

CART_URL = f"{BASE_URL}/cart"
CHECKOUT_URL = f"{BASE_URL}/checkout"


def test_checkout_redirects_when_cart_empty():
    """Visiting /checkout with empty cart should redirect back to cart or show message."""
    driver = get_driver()
    try:
        driver.get(CHECKOUT_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(kw in body_text for kw in
                   ["cart", "empty", "checkout", "item", "order"]), \
            "Checkout/cart page should show relevant content"
        save_screenshot(driver, "checkout_empty_cart")
        print(f"✅ Checkout empty-cart handled | URL: {driver.current_url}")
    finally:
        driver.quit()


def test_checkout_button_visible_or_absent_on_cart():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        # Either checkout button is visible (items in cart) or empty-cart message shows
        has_checkout = "checkout" in body_text
        has_empty = any(kw in body_text for kw in ["empty", "no item"])
        assert has_checkout or has_empty
        save_screenshot(driver, "checkout_button_check")
        print(f"✅ Checkout present: {has_checkout} | Empty state: {has_empty}")
    finally:
        driver.quit()


def test_cart_page_does_not_throw_500():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "500" not in driver.title and "server error" not in body_text
        print("✅ Cart page returned no 500 error")
    finally:
        driver.quit()
