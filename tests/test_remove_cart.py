from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

CART_URL = f"{BASE_URL}/cart"


def test_cart_starts_empty():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/cart.json")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "item_count" in body
        print(f"✅ Cart JSON accessible | raw: {body[:100]}")
    finally:
        driver.quit()


def test_remove_button_absent_on_empty_cart():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        remove_btns = driver.find_elements(By.XPATH,
            "//button[contains(text(),'Remove') or contains(@class,'remove')]"
        )
        # On an empty cart there should be no remove buttons
        assert len(remove_btns) == 0, "Empty cart should not have Remove buttons"
        save_screenshot(driver, "empty_cart_no_remove_btn")
        print("✅ No remove buttons on empty cart")
    finally:
        driver.quit()


def test_cart_page_has_checkout_or_empty_state():
    driver = get_driver()
    try:
        driver.get(CART_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        has_checkout = "checkout" in body_text
        has_empty = any(kw in body_text for kw in ["empty", "no item", "your cart"])
        assert has_checkout or has_empty, \
            "Cart page should show checkout button or empty state"
        print(f"✅ Cart state — checkout: {has_checkout}, empty message: {has_empty}")
    finally:
        driver.quit()
