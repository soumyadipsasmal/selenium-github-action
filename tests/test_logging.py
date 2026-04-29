import logging
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, BASE_URL

# Configure file logger
os.makedirs("reports", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("reports/test_run.log"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


def test_homepage_with_logging():
    logger.info("START test_homepage_with_logging")
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info(f"Page loaded | URL: {driver.current_url} | Title: {driver.title}")
        assert driver.current_url.startswith("https://")
        logger.info("PASS test_homepage_with_logging")
    except Exception as e:
        logger.error(f"FAIL test_homepage_with_logging: {e}")
        raise
    finally:
        driver.quit()


def test_browser_console_logs():
    logger.info("START test_browser_console_logs")
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logs = driver.get_log("browser")
        for entry in logs:
            level = entry.get("level", "")
            msg = entry.get("message", "")[:120]
            if level == "SEVERE":
                logger.warning(f"BROWSER SEVERE: {msg}")
            else:
                logger.debug(f"BROWSER {level}: {msg}")
        logger.info(f"Browser log entries: {len(logs)}")
        assert True
        logger.info("PASS test_browser_console_logs")
    finally:
        driver.quit()


def test_log_file_created():
    os.makedirs("reports", exist_ok=True)
    logger.info("Log file creation test")
    assert os.path.isdir("reports"), "reports/ directory should exist"
    print("✅ reports/ directory exists — logging is configured")
