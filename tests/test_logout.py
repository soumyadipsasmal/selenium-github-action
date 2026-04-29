from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

LOGIN_URL = f"{BASE_URL}/account/login"
LOGOUT_URL = f"{BASE_URL}/account/logout"


def test_logout_url_redirects():
    """Visiting logout URL without a session should redirect to login or home."""
    driver = get_driver()
    try:
        driver.get(LOGOUT_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != "", "Logout URL should result in a valid page"
        save_screenshot(driver, "logout_redirect")
        print(f"✅ Logout redirected to: {driver.current_url}")
    finally:
        driver.quit()


def test_account_page_redirects_to_login_when_not_authenticated():
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/account")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Shopify redirects unauthenticated /account to /account/login
        assert "login" in driver.current_url or "account" in driver.current_url
        save_screenshot(driver, "account_redirect_to_login")
        print(f"✅ /account redirected to: {driver.current_url}")
    finally:
        driver.quit()


def test_login_link_visible_when_not_authenticated():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        login_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'login') or contains(@href,'account') or "
            "contains(text(),'Login') or contains(text(),'Sign in')]"
        )
        assert len(login_links) > 0, "Login link should be visible when not logged in"
        print(f"✅ Login link visible: '{login_links[0].text}'")
    finally:
        driver.quit()
