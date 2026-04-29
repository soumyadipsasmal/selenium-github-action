from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_anvi_homepage():

    options = Options()

    # Headless mode
    options.add_argument("--headless=new")

    # Linux fixes
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Faster loading
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # Page load timeout
    driver.set_page_load_timeout(30)

    try:
        # Open website
        driver.get("https://anvicouture.com/")

        time.sleep(5)

        # Validate title
        assert "Anvi" in driver.title

        # Save screenshot
        driver.save_screenshot("screenshots/anvi_homepage.png")

        print("Website loaded successfully")

    finally:
        driver.quit()
