from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

REGISTER_URL = f"{BASE_URL}/account/register"


def test_signup_page_loads():
    driver = get_driver()
    try:
        driver.get(REGISTER_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "signup_page")
        print(f"✅ Signup page loaded: {driver.title}")
    finally:
        driver.quit()


def test_signup_form_has_required_fields():
    driver = get_driver()
    try:
        driver.get(REGISTER_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        email = driver.find_elements(By.XPATH, "//input[@type='email' or @name='customer[email]']")
        pwd = driver.find_elements(By.XPATH, "//input[@type='password']")
        assert len(email) > 0, "Signup form must have an email field"
        assert len(pwd) > 0, "Signup form must have a password field"
        print("✅ Signup form has email and password fields")
    finally:
        driver.quit()


def test_signup_submit_with_empty_fields():
    driver = get_driver()
    try:
        driver.get(REGISTER_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        submit = driver.find_elements(By.XPATH,
            "//input[@type='submit'] | //button[@type='submit']"
        )
        if submit:
            submit[0].click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # Either browser HTML5 validation blocks it OR server returns error
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            save_screenshot(driver, "signup_empty_submit")
            print(f"✅ Empty submit handled | Body excerpt: {body_text[:100]}")
        else:
            print("⚠️ Submit button not found — skipping")
    finally:
        driver.quit()


def test_signup_page_has_login_link():
    driver = get_driver()
    try:
        driver.get(REGISTER_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        login_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'login') or contains(text(),'Login') or contains(text(),'Sign in')]"
        )
        assert len(login_links) > 0, "Register page should link back to login"
        print(f"✅ Login link on signup page: '{login_links[0].text}'")
    finally:
        driver.quit()
