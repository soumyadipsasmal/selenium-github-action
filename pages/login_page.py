from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object Model for https://anvicouture.com/account/login"""

    URL          = "https://anvicouture.com/account/login"
    RECOVER_URL  = "https://anvicouture.com/account/login#recover"

    # Locators
    BODY            = (By.TAG_NAME, "body")
    EMAIL_INPUT     = (By.XPATH, "//input[@type='email' or @name='customer[email]']")
    PASSWORD_INPUT  = (By.XPATH, "//input[@type='password']")
    SUBMIT_BTN      = (By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
    ERROR_MSG       = (By.XPATH,
                       "//*[contains(@class,'error') or contains(@class,'notice') "
                       "or contains(@id,'error')]")
    FORGOT_LINK     = (By.XPATH,
                       "//a[contains(@href,'recover') or contains(text(),'Forgot') "
                       "or contains(text(),'forgot')]")
    SIGNUP_LINK     = (By.XPATH,
                       "//a[contains(@href,'register') or contains(text(),'Sign up') "
                       "or contains(text(),'Create')]")
    RECOVER_EMAIL   = (By.XPATH,
                       "//input[@type='email' and not(@name='customer[email]')]"
                       " | //input[@id='RecoverEmail']")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)

    # ── Navigation ────────────────────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def open_recover(self):
        self.driver.get(self.RECOVER_URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    # ── Actions ───────────────────────────────────────────────────────────
    def enter_email(self, email: str):
        field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        field.clear()
        field.send_keys(email)
        return self

    def enter_password(self, password: str):
        field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        field.clear()
        field.send_keys(password)
        return self

    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def login(self, email: str, password: str):
        """Fill form and submit in one call."""
        return self.enter_email(email).enter_password(password).click_submit()

    def click_forgot_password(self):
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_LINK)).click()
        return self

    def click_signup_link(self):
        self.wait.until(EC.element_to_be_clickable(self.SIGNUP_LINK)).click()
        return self

    # ── State checks ──────────────────────────────────────────────────────
    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
            return True
        except Exception:
            return False

    def has_email_field(self) -> bool:
        return len(self.driver.find_elements(*self.EMAIL_INPUT)) > 0

    def has_password_field(self) -> bool:
        return len(self.driver.find_elements(*self.PASSWORD_INPUT)) > 0

    def has_forgot_link(self) -> bool:
        return len(self.driver.find_elements(*self.FORGOT_LINK)) > 0

    def has_signup_link(self) -> bool:
        return len(self.driver.find_elements(*self.SIGNUP_LINK)) > 0

    def get_error_message(self) -> str:
        try:
            el = self.wait.until(EC.visibility_of_element_located(self.ERROR_MSG))
            return el.text.strip()
        except Exception:
            return ""

    def is_error_shown(self) -> bool:
        return bool(self.get_error_message())

    def get_current_url(self) -> str:
        return self.driver.current_url
