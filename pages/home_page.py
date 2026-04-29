from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    """Page Object Model for https://anvicouture.com homepage."""

    URL = "https://anvicouture.com"

    # Locators
    BODY             = (By.TAG_NAME, "body")
    HEADER           = (By.TAG_NAME, "header")
    FOOTER           = (By.TAG_NAME, "footer")
    NAV              = (By.TAG_NAME, "nav")
    ALL_IMAGES       = (By.TAG_NAME, "img")
    ALL_LINKS        = (By.TAG_NAME, "a")
    CART_LINK        = (By.XPATH, "//a[contains(@href,'cart') or contains(@class,'cart')]")
    LOGO             = (By.XPATH, "//*[contains(@class,'logo') or contains(@id,'logo')]")
    NAV_LINKS        = (By.CSS_SELECTOR, "nav a")
    COLLECTION_LINK  = (By.XPATH, "//a[contains(@href,'/collections')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)

    # ── Navigation ────────────────────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    # ── Getters ───────────────────────────────────────────────────────────
    def get_title(self) -> str:
        return self.driver.title

    def get_url(self) -> str:
        return self.driver.current_url

    def get_all_links(self) -> list[str]:
        return [
            a.get_attribute("href")
            for a in self.driver.find_elements(*self.ALL_LINKS)
            if a.get_attribute("href")
        ]

    def get_image_count(self) -> int:
        return len(self.driver.find_elements(*self.ALL_IMAGES))

    def get_nav_link_texts(self) -> list[str]:
        return [a.text.strip() for a in self.driver.find_elements(*self.NAV_LINKS) if a.text.strip()]

    # ── State checks ──────────────────────────────────────────────────────
    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.BODY))
            return True
        except Exception:
            return False

    def is_https(self) -> bool:
        return self.driver.current_url.startswith("https://")

    def has_header(self) -> bool:
        return len(self.driver.find_elements(*self.HEADER)) > 0

    def has_footer(self) -> bool:
        return len(self.driver.find_elements(*self.FOOTER)) > 0

    def has_navigation(self) -> bool:
        return len(self.driver.find_elements(*self.NAV)) > 0

    def has_cart_link(self) -> bool:
        return len(self.driver.find_elements(*self.CART_LINK)) > 0

    def has_logo(self) -> bool:
        return len(self.driver.find_elements(*self.LOGO)) > 0

    # ── Actions ───────────────────────────────────────────────────────────
    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()
        return self

    def go_to_collections(self):
        link = self.wait.until(EC.element_to_be_clickable(self.COLLECTION_LINK))
        link.click()
        return self

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        return self

    def get_page_height(self) -> int:
        return self.driver.execute_script("return document.body.scrollHeight;")

    def save_screenshot(self, path: str):
        self.driver.save_screenshot(path)
