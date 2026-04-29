from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL
import os


def test_anvi_homepage():
    driver = get_driver()
    try:
        driver.get(BASE_URL)

        # Wait for <body> to load — doesn't depend on exact title text
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        actual_title = driver.title
        print(f"\n📄 Actual page title: '{actual_title}'")

        assert actual_title != "", "Page title is empty — possible bot block"

        save_screenshot(driver, "anvi_homepage")
        print("✅ Screenshot saved → screenshots/anvi_homepage.png")

    finally:
        driver.quit()

# ✅ NO bare function call — pytest finds test_ functions automatically
