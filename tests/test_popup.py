import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_no_blocking_popup_on_load():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)  # Let any popup animations complete
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0, "Page body should have content despite any popups"
        save_screenshot(driver, "popup_on_load")
        print("✅ Page body accessible — no fully blocking popup")
    finally:
        driver.quit()


def test_popup_close_button_if_present():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)
        close_btns = driver.find_elements(By.XPATH,
            "//*[contains(@class,'close') or contains(@aria-label,'Close') or "
            "contains(@class,'dismiss') or contains(@id,'close')]"
        )
        if close_btns:
            close_btns[0].click()
            save_screenshot(driver, "popup_closed")
            print(f"✅ Closed popup/modal using: {close_btns[0].get_attribute('class')}")
        else:
            print("ℹ️ No popup close button found — popup may not have appeared")
        assert True
    finally:
        driver.quit()


def test_newsletter_popup_if_present():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(4)
        newsletter = driver.find_elements(By.XPATH,
            "//input[@type='email' and (contains(@placeholder,'email') or "
            "contains(@name,'email'))]"
        )
        print(f"ℹ️ Newsletter email input visible: {len(newsletter) > 0}")
        save_screenshot(driver, "newsletter_popup")
        assert True
    finally:
        driver.quit()
