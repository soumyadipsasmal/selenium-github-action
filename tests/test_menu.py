from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_nav_menu_present():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a")
        assert len(nav_links) > 0, "Navigation menu should have links"
        print(f"✅ Nav menu has {len(nav_links)} links")
    finally:
        driver.quit()


def test_nav_links_have_href():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a")
        for link in nav_links:
            href = link.get_attribute("href")
            assert href and href.strip() != "", f"Nav link '{link.text}' has no href"
        print(f"✅ All {len(nav_links)} nav links have valid href attributes")
    finally:
        driver.quit()


def test_collections_link_in_menu():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        menu_text = driver.find_element(By.TAG_NAME, "nav").text.lower()
        assert any(kw in menu_text for kw in ["collection", "shop", "product", "catalog"]), \
            "Menu should have a collections or shop link"
        print("✅ Collections/shop link found in menu")
    finally:
        driver.quit()


def test_menu_home_link_navigates():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        home_links = driver.find_elements(By.XPATH,
            "//nav//a[contains(@href,'anvicouture.com') or @href='/' or @href='']"
        )
        assert len(home_links) > 0, "Menu should contain a home/logo link"
        save_screenshot(driver, "menu_home_link")
        print("✅ Home link present in menu")
    finally:
        driver.quit()
