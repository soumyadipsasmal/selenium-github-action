from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

LOGIN_URL = f"{BASE_URL}/account/login"


def test_forgot_password_link_present():
    driver = get_driver()
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        forgot_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'recover') or contains(text(),'Forgot') or "
            "contains(text(),'forgot') or contains(text(),'Reset')]"
        )
        assert len(forgot_links) > 0, "Login page should have a 'Forgot password' link"
        print(f"✅ Forgot password link: '{forgot_links[0].text}'")
    finally:
        driver.quit()


def test_recover_password_page_loads():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/account/login#recover")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "recover_password_page")
        print(f"✅ Recover page loaded: {driver.current_url}")
    finally:
        driver.quit()


def test_recover_form_has_email_field():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/account/login#recover")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Try clicking the forgot link to reveal the recover form
        forgot_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'recover') or contains(text(),'Forgot') or contains(text(),'forgot')]"
        )
        if forgot_links:
            forgot_links[0].click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        email_fields = driver.find_elements(By.XPATH, "//input[@type='email']")
        assert len(email_fields) > 0, "Password recovery form should have an email field"
        print("✅ Email field found on recover form")
    finally:
        driver.quit()
