from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_footer_exists():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        footer = driver.find_elements(By.TAG_NAME, "footer")
        assert len(footer) > 0, "Page should have a <footer> element"
        print("✅ Footer element found")
    finally:
        driver.quit()


def test_footer_has_links():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        footer = driver.find_element(By.TAG_NAME, "footer")
        links = footer.find_elements(By.TAG_NAME, "a")
        assert len(links) > 0, "Footer should contain links"
        print(f"✅ Footer has {len(links)} links")
    finally:
        driver.quit()


def test_footer_visible_in_viewport_after_scroll():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        footer = driver.find_element(By.TAG_NAME, "footer")
        assert footer.is_displayed(), "Footer should be visible after scrolling to bottom"
        save_screenshot(driver, "footer_visible")
        print("✅ Footer visible after scroll")
    finally:
        driver.quit()


def test_footer_copyright_text():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        footer_text = driver.find_element(By.TAG_NAME, "footer").text.lower()
        assert any(kw in footer_text for kw in ["©", "copyright", "anvi", "rights"]), \
            "Footer should contain copyright or brand text"
        print("✅ Footer contains brand/copyright text")
    finally:
        driver.quit()
