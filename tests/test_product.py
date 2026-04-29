from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

COLLECTIONS_URL = f"{BASE_URL}/collections/all"


def test_product_page_loads():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "collection" in driver.current_url.lower() or driver.title != ""
        print(f"✅ Collections page loaded: {driver.title}")
        save_screenshot(driver, "collections_page")
    finally:
        driver.quit()


def test_products_are_listed():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        products = driver.find_elements(By.XPATH,
            "//*[contains(@class,'product') or contains(@class,'card') or contains(@class,'item')]"
        )
        assert len(products) > 0, "Products should be listed on the collections page"
        print(f"✅ Found {len(products)} product elements")
    finally:
        driver.quit()


def test_product_images_present():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        assert len(images) > 0, "Product images should be present"
        print(f"✅ Found {len(images)} images on collections page")
    finally:
        driver.quit()


def test_product_links_clickable():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        product_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'/products/')]"
        )
        assert len(product_links) > 0, "Should have clickable product links"
        first_href = product_links[0].get_attribute("href")
        print(f"✅ Found {len(product_links)} product links | First: {first_href}")
    finally:
        driver.quit()


def test_open_first_product():
    driver = get_driver()
    try:
        driver.get(COLLECTIONS_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        product_links = driver.find_elements(By.XPATH, "//a[contains(@href,'/products/')]")
        assert product_links, "No product links found"
        product_links[0].click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "/products/" in driver.current_url
        save_screenshot(driver, "product_detail")
        print(f"✅ Product detail page loaded: {driver.current_url}")
    finally:
        driver.quit()
