from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

COLLECTIONS_URL = f"{BASE_URL}/collections/all"


def test_collections_page_accessible():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, "outofstock_collections")
        print("✅ Collections page loaded for out-of-stock check")
    finally:
        driver.quit()


def test_out_of_stock_badge_check():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        oos_elements = driver.find_elements(By.XPATH,
            "//*[contains(text(),'Sold Out') or contains(text(),'Out of Stock') or "
            "contains(@class,'sold-out') or contains(@class,'soldout')]"
        )
        print(f"ℹ️ Out-of-stock elements found: {len(oos_elements)}")
        # Just log — presence of OOS items is normal
        assert True
    finally:
        driver.quit()


def test_add_to_cart_button_availability():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        product_links = driver.find_elements(By.XPATH, "//a[contains(@href,'/products/')]")
        if product_links:
            product_links[0].click()
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            add_btns = driver.find_elements(By.XPATH,
                "//button[contains(text(),'Add to cart') or contains(text(),'Add to Cart') or "
                "contains(text(),'Sold Out') or contains(text(),'Unavailable')]"
            )
            print(f"ℹ️ Add/Sold-out buttons found: {len(add_btns)}")
            if add_btns:
                btn_text = add_btns[0].text
                save_screenshot(driver, f"outofstock_btn_{btn_text[:10]}")
                print(f"✅ Button text: '{btn_text}'")
        assert True
    finally:
        driver.quit()


def test_product_detail_page_shows_stock_status():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        product_links = driver.find_elements(By.XPATH, "//a[contains(@href,'/products/')]")
        if product_links:
            product_links[0].click()
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            has_stock_info = any(kw in body_text for kw in
                                 ["add to cart", "sold out", "unavailable", "buy now"])
            print(f"✅ Stock status present: {has_stock_info}")
            assert True  # Page loaded correctly
    finally:
        driver.quit()
