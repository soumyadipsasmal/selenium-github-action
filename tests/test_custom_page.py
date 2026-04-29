from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

PAGES = [
    ("About", f"{BASE_URL}/pages/about"),
    ("Contact", f"{BASE_URL}/pages/contact"),
    ("FAQ", f"{BASE_URL}/pages/faq"),
    ("Shipping", f"{BASE_URL}/pages/shipping-policy"),
    ("Returns", f"{BASE_URL}/pages/refund-policy"),
    ("Privacy Policy", f"{BASE_URL}/policies/privacy-policy"),
]


def test_about_page_loads():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/pages/about")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "custom_about_page")
        print(f"✅ About page: {driver.current_url}")
    finally:
        driver.quit()


def test_contact_page_loads():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/pages/contact")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "custom_contact_page")
        print(f"✅ Contact page: {driver.current_url}")
    finally:
        driver.quit()


def test_privacy_policy_page_loads():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/policies/privacy-policy")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(kw in body_text for kw in ["privacy", "data", "information", "policy"]), \
            "Privacy policy page should contain relevant text"
        save_screenshot(driver, "custom_privacy_page")
        print("✅ Privacy policy page loaded with relevant content")
    finally:
        driver.quit()


def test_refund_policy_page_loads():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/policies/refund-policy")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "custom_refund_page")
        print(f"✅ Refund policy page: {driver.current_url}")
    finally:
        driver.quit()


def test_404_page_for_invalid_url():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/pages/this-page-does-not-exist-xyz123")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(kw in body_text for kw in ["not found", "404", "page", "error"]), \
            "Invalid page should show 404 or 'not found' message"
        save_screenshot(driver, "custom_404_page")
        print("✅ 404 page shown for invalid URL")
    finally:
        driver.quit()
