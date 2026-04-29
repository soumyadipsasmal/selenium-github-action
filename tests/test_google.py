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

    # ✅ No ChromeDriverManager needed — Selenium 4.6+ manages it automatically
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)

    try:
        driver.get("https://anvicouture.com/")

        # ✅ Wait for title to be populated (JS-rendered), up to 15s
        WebDriverWait(driver, 15).until(
            EC.title_contains("Anvi")
        )

        print(f"Title: {driver.title}")
        assert "Anvi" in driver.title

        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots/anvi_homepage.png")
        print("✅ Website loaded successfully")
        print("✅ Screenshot saved → screenshots/anvi_homepage.png")

    finally:
        driver.quit()

test_anvi_homepage()