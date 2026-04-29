from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class SearchPage:
    """Page Object Model for https://anvicouture.com/search"""

    URL      = "https://anvicouture.com/search"
    BASE_URL = "https://anvicouture.com"

    # Locators
    BODY            = (By.TAG_NAME, "body")
    SEARCH_INPUT    = (By.XPATH,
                       "//input[@type='search' or contains(@name,'q') or contains(@name,'search') "
                       "or contains(@id,'search') or contains(@placeholder,'Search')]")
    SEARCH_SUBMIT   = (By.XPATH,
                       "//button[@type='submit' and ancestor::form[contains(@action,'search')]] "
                       "| //input[@type='submit' and ancestor::form[contains(@action,'search')]]")
    RESULT_ITEMS    = (By.XPATH,
                       "//*[contains(@class,'search-result') or contains(@class,'result') "
                       "or contains(@class,'product')]")
    RESULT_LINKS    = (By.XPATH, "//a[contains(@href,'/products/')]")
    NO_RESULT_MSG   = (By.XPATH,
                       "//*[contains(text(),'no result') or contains(text(),'No result') "
                       "or contains(text(),'not found') or contains(text(),'0 result')]")
    RESULT_COUNT    = (By.XPATH,
                       "//*[contains(@class,'count') or contains(text(),'result')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)

    # ── Navigation ────────────────────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def search_via_url(self, query: str):
        """Fastest way — go directly to the search URL with query param."""
        self.driver.get(f"{self.URL}?q={query}")
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def search_via_form(self, query: str):
        """Type into search box and submit."""
        field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        field.clear()
        field.send_keys(query)
        field.send_keys(Keys.RETURN)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def open_search_icon(self):
        """Click the header search icon to reveal the search box."""
        search_icons = self.driver.find_elements(By.XPATH,
            "//button[contains(@aria-label,'Search') or contains(@class,'search')] "
            "| //a[contains(@href,'search') and not(contains(@href,'?'))]"
        )
        if search_icons:
            search_icons[0].click()
        return self

    # ── Getters ───────────────────────────────────────────────────────────
    def get_result_count(self) -> int:
        return len(self.driver.find_elements(*self.RESULT_LINKS))

    def get_result_titles(self) -> list[str]:
        return [
            el.text.strip()
            for el in self.driver.find_elements(*self.RESULT_ITEMS)
            if el.text.strip()
        ]

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_search_input_value(self) -> str:
        try:
            field = self.driver.find_element(*self.SEARCH_INPUT)
            return field.get_attribute("value") or ""
        except Exception:
            return ""

    # ── State checks ──────────────────────────────────────────────────────
    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.BODY))
            return True
        except Exception:
            return False

    def has_search_input(self) -> bool:
        return len(self.driver.find_elements(*self.SEARCH_INPUT)) > 0

    def has_results(self) -> bool:
        return self.get_result_count() > 0

    def shows_no_results_message(self) -> bool:
        no_msg = len(self.driver.find_elements(*self.NO_RESULT_MSG)) > 0
        body   = self.driver.find_element(*self.BODY).text.lower()
        return no_msg or any(kw in body for kw in
                             ["no result", "not found", "0 result", "nothing"])
