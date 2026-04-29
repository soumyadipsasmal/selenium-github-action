from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


def test_anvi_homepage():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)

    try:
        driver.get("https://anvicouture.com/")

        # ✅ Wait for <body> to load — doesn't depend on exact title text
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        actual_title = driver.title
        print(f"\n📄 Actual page title: '{actual_title}'")

        # ✅ Use the real title — update this after you see what prints above
        assert actual_title != "", f"Page title is empty — possible bot block"

        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots/anvi_homepage.png")
        print("✅ Screenshot saved → screenshots/anvi_homepage.png")

    finally:
        driver.quit()

# ✅ NO bare function call here — pytest finds test_ functions automatically