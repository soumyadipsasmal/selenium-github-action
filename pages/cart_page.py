from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Page Object Model for https://anvicouture.com/cart"""

    URL      = "https://anvicouture.com/cart"
    JSON_URL = "https://anvicouture.com/cart.json"

    # Locators
    BODY               = (By.TAG_NAME, "body")
    CHECKOUT_BTN       = (By.XPATH,
                          "//input[@name='checkout'] | //button[contains(text(),'Checkout')] "
                          "| //a[contains(text(),'Checkout') or contains(@href,'checkout')]")
    CONTINUE_BTN       = (By.XPATH,
                          "//a[contains(text(),'Continue') or contains(text(),'Shop') "
                          "or contains(@href,'collection') or contains(@href,'all')]")
    REMOVE_BTNS        = (By.XPATH,
                          "//button[contains(text(),'Remove') or contains(@class,'remove')] "
                          "| //a[contains(@href,'/cart/change')]")
    QUANTITY_INPUTS    = (By.XPATH,
                          "//input[@type='number' or contains(@name,'quantity') "
                          "or contains(@class,'quantity')]")
    CART_ITEMS         = (By.XPATH,
                          "//*[contains(@class,'cart__item') or contains(@class,'cart-item') "
                          "or contains(@class,'line-item')]")
    EMPTY_MSG          = (By.XPATH,
                          "//*[contains(text(),'empty') or contains(text(),'Empty') "
                          "or contains(@class,'empty')]")
    DISCOUNT_INPUT     = (By.XPATH,
                          "//input[contains(@name,'discount') or contains(@id,'discount') "
                          "or contains(@placeholder,'Discount') or contains(@placeholder,'coupon')]")
    CART_TOTAL         = (By.XPATH,
                          "//*[contains(@class,'total') or contains(@class,'Total') "
                          "or contains(@id,'cart-total')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)

    # ── Navigation ────────────────────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def open_cart_json(self):
        self.driver.get(self.JSON_URL)
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    # ── Getters ───────────────────────────────────────────────────────────
    def get_cart_json_text(self) -> str:
        self.open_cart_json()
        return self.driver.find_element(*self.BODY).text

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_quantity_inputs(self):
        return self.driver.find_elements(*self.QUANTITY_INPUTS)

    def get_cart_total_text(self) -> str:
        try:
            return self.driver.find_element(*self.CART_TOTAL).text.strip()
        except Exception:
            return ""

    def get_current_url(self) -> str:
        return self.driver.current_url

    # ── State checks ──────────────────────────────────────────────────────
    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.BODY))
            return True
        except Exception:
            return False

    def is_empty(self) -> bool:
        body_text = self.driver.find_element(*self.BODY).text.lower()
        return any(kw in body_text for kw in ["empty", "no item", "your cart is"])

    def has_checkout_button(self) -> bool:
        return len(self.driver.find_elements(*self.CHECKOUT_BTN)) > 0

    def has_continue_shopping(self) -> bool:
        return len(self.driver.find_elements(*self.CONTINUE_BTN)) > 0

    def has_remove_buttons(self) -> bool:
        return len(self.driver.find_elements(*self.REMOVE_BTNS)) > 0

    def has_discount_input(self) -> bool:
        return len(self.driver.find_elements(*self.DISCOUNT_INPUT)) > 0

    # ── Actions ───────────────────────────────────────────────────────────
    def click_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def click_continue_shopping(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.BODY))
        return self

    def enter_discount_code(self, code: str):
        field = self.wait.until(EC.visibility_of_element_located(self.DISCOUNT_INPUT))
        field.clear()
        field.send_keys(code)
        return self

    def update_quantity(self, index: int, qty: int):
        inputs = self.get_quantity_inputs()
        if index < len(inputs):
            inputs[index].clear()
            inputs[index].send_keys(str(qty))
        return self
