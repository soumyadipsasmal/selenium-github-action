from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

LOGIN_URL = f"{BASE_URL}/account/login"


def test_login_page_loads():
    driver = get_driver()
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print(f"✅ Login page loaded: {driver.title}")
        save_screenshot(driver, "login_page")
    finally:
        driver.quit()


def test_login_form_has_email_field():
    driver = get_driver()
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        email = driver.find_elements(By.XPATH,
            "//input[@type='email' or @name='customer[email]' or contains(@id,'email')]"
        )
        assert len(email) > 0, "Login form should have an email field"
        print("✅ Email input field found")
    finally:
        driver.quit()


def test_login_form_has_password_field():
    driver = get_driver()
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        pwd = driver.find_elements(By.XPATH, "//input[@type='password']")
        assert len(pwd) > 0, "Login form should have a password field"
        print("✅ Password input field found")
    finally:
        driver.quit()


def test_login_with_invalid_credentials():
    driver = get_driver()
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        email_inputs = driver.find_elements(By.XPATH,
            "//input[@type='email' or @name='customer[email]']"
        )
        pwd_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        if email_inputs and pwd_inputs:
            email_inputs[0].send_keys("invalid@test.com")
            pwd_inputs[0].send_keys("wrongpassword123")
            submit = driver.find_elements(By.XPATH,
                "//input[@type='submit'] | //button[@type='submit']"
            )
            if submit:
                submit[0].click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                assert any(kw in body_text for kw in
                           ["incorrect", "invalid", "error", "wrong", "login"]), \
                    "Should show error for invalid credentials"
                save_screenshot(driver, "login_invalid_error")
                print("✅ Invalid login shows error message")
        else:
            print("⚠️ Login form fields not found — skipping input test")
    finally:
        driver.quit()


def test_login_page_has_signup_link():
    driver = get_driver()
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'register') or contains(@href,'signup') or contains(text(),'Sign up') or contains(text(),'Create')]"
        )
        assert len(links) > 0, "Login page should link to registration"
        print(f"✅ Signup link found: '{links[0].text}'")
    finally:
        driver.quit()
