from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    """Page Object Model for product listing and detail pages on anvicouture.com"""

    COLLECTIONS_URL = "https://anvicouture.com/collections/all"

    # Locators — collections listing
    BODY             = (By.TAG_NAME, "body")
    ALL_IMAGES       = (By.TAG_NAME, "img")
    PRODUCT_LINKS    = (By.XPATH, "//a[contains(@href,'/products/')]")
    PRODUCT_CARDS    = (By.XPATH,
                        "//*[contains(@class,'product') or contains(@class,'card') "
                        "or contains(@class,'item')]")
    SORT_SELECT      = (By.XPATH,
                        "//select[contains(@id,'sort') or contains(@name,'sort') "
                        "or contains(@class,'sort')]")

    # Locators — product detail
    PRODUCT_TITLE    = (By.XPATH,
                        "//*[contains(@class,'product__title') or contains(@class,'product-title') "
                        "or contains(@itemprop,'name') or (self::h1)]")
    PRODUCT_PRICE    = (By.XPATH,
                        "//*[contains(@class,'price') or contains(@class,'Price') "
                        "or contains(@itemprop,'price')]")
    PRODUCT_DESC     = (By.XPATH,
                        "//*[contains(@class,'description') or contains(@class,'product__desc') "
                        "or contains(@itemprop,'description')]")
    ADD_TO_CART_BTN  = (By.XPATH,
                        "//button[contains(text(),'Add to cart') or "
                        "contains(text(),'Add to Cart') or contains(@name,'add')]")
    SOLD_OUT_BTN     = (By.XPATH,
                        "//button[contains(text(),'Sold Out') or "
                        "contains(text(),'Unavailable')]")
    QUANTITY_INPUT   = (By.XPATH,
                        "//input[@type='number' or contains(@id,'Quantity') "
                        "or contains(@name,'quantity')]")
    VARIANT_OPTIONS  = (By.XPATH,
                        "//select[contains(@name,'options') or contains(@id,'option')] "
                        "| //input[@type='radio' and contains(@name,'option')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)

    # ── Navigation ────────────────────────────────────────────────────────
    def open_collections(self):
        self.driver.get(self.COLLECTIONS_URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def open_collection(self, slug: str):
        self.driver.get(f"https://anvicouture.com/collections/{slug}")
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def open_first_product(self):
        links = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_LINKS))
        links[0].click()
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def open_product_by_index(self, index: int):
        links = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_LINKS))
        links[index].click()
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    # ── Listing page getters ──────────────────────────────────────────────
    def get_product_count(self) -> int:
        return len(self.driver.find_elements(*self.PRODUCT_LINKS))

    def get_product_urls(self) -> list[str]:
        return [
            a.get_attribute("href")
            for a in self.driver.find_elements(*self.PRODUCT_LINKS)
            if a.get_attribute("href")
        ]

    def get_image_count(self) -> int:
        return len(self.driver.find_elements(*self.ALL_IMAGES))

    # ── Detail page getters ───────────────────────────────────────────────
    def get_product_title(self) -> str:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PRODUCT_TITLE)
            ).text.strip()
        except Exception:
            return ""

    def get_product_price(self) -> str:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PRODUCT_PRICE)
            ).text.strip()
        except Exception:
            return ""

    def get_product_description(self) -> str:
        try:
            return self.driver.find_element(*self.PRODUCT_DESC).text.strip()
        except Exception:
            return ""

    # ── State checks ──────────────────────────────────────────────────────
    def is_collections_loaded(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.BODY))
            return "collection" in self.driver.current_url or self.get_product_count() > 0
        except Exception:
            return False

    def is_product_page(self) -> bool:
        return "/products/" in self.driver.current_url

    def is_add_to_cart_available(self) -> bool:
        return len(self.driver.find_elements(*self.ADD_TO_CART_BTN)) > 0

    def is_sold_out(self) -> bool:
        return len(self.driver.find_elements(*self.SOLD_OUT_BTN)) > 0

    def has_variant_options(self) -> bool:
        return len(self.driver.find_elements(*self.VARIANT_OPTIONS)) > 0

    # ── Actions ───────────────────────────────────────────────────────────
    def click_add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()
        return self

    def sort_by(self, sort_value: str):
        """Sort value examples: 'price-ascending', 'price-descending', 'created-descending'"""
        self.driver.get(f"{self.COLLECTIONS_URL}?sort_by={sort_value}")
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def get_current_url(self) -> str:
        return self.driver.current_url
