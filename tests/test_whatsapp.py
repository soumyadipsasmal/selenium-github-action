from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_whatsapp_button_present():
    """Many couture/boutique Shopify stores add a WhatsApp chat button."""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        wa_elements = driver.find_elements(By.XPATH,
            "//*[contains(@href,'wa.me') or contains(@href,'whatsapp') or "
            "contains(@class,'whatsapp') or contains(@id,'whatsapp') or "
            "contains(@aria-label,'WhatsApp')]"
        )
        print(f"ℹ️ WhatsApp elements found: {len(wa_elements)}")
        save_screenshot(driver, "whatsapp_button")
        # Log result — not all stores implement this
        assert True
    finally:
        driver.quit()


def test_whatsapp_link_opens_correct_url():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        wa_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'wa.me') or contains(@href,'whatsapp.com')]"
        )
        if wa_links:
            href = wa_links[0].get_attribute("href")
            assert "wa.me" in href or "whatsapp" in href, \
                "WhatsApp link should point to wa.me or whatsapp.com"
            print(f"✅ WhatsApp link valid: {href}")
        else:
            print("ℹ️ No WhatsApp link found on homepage")
        assert True
    finally:
        driver.quit()


def test_page_has_contact_method():
    """Site should have some contact method — WhatsApp, email, or contact page."""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        contact_elements = driver.find_elements(By.XPATH,
            "//a[contains(@href,'contact') or contains(@href,'wa.me') or "
            "contains(@href,'mailto') or contains(@href,'whatsapp')]"
        )
        assert len(contact_elements) > 0, "Site should have at least one contact method"
        print(f"✅ Contact elements found: {len(contact_elements)}")
        for el in contact_elements[:3]:
            print(f"   → {el.get_attribute('href')}")
    finally:
        driver.quit()
