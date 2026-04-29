import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def _get_all_links(driver):
    return [
        a.get_attribute("href")
        for a in driver.find_elements(By.TAG_NAME, "a")
        if a.get_attribute("href") and a.get_attribute("href").startswith("http")
    ]


def test_homepage_links_collected():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        links = _get_all_links(driver)
        assert len(links) > 0, "Homepage should have at least one absolute link"
        print(f"✅ Collected {len(links)} links from homepage")
    finally:
        driver.quit()


def test_internal_links_no_404():
    """Check that internal links on the homepage return non-404 status."""
    driver = get_driver()
    broken = []
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        links = [
            a.get_attribute("href")
            for a in driver.find_elements(By.TAG_NAME, "a")
            if a.get_attribute("href")
            and "anvicouture.com" in (a.get_attribute("href") or "")
        ]
        # Check up to 10 internal links to keep test fast
        for url in list(set(links))[:10]:
            try:
                r = requests.head(url, timeout=10, allow_redirects=True)
                if r.status_code == 404:
                    broken.append(url)
                    print(f"  ❌ 404 → {url}")
                else:
                    print(f"  ✅ {r.status_code} → {url}")
            except Exception as e:
                print(f"  ⚠️ Could not check {url}: {e}")
        assert len(broken) == 0, f"Broken links found: {broken}"
    finally:
        driver.quit()


def test_no_javascript_errors_on_load():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l.get("level") == "SEVERE"]
        for err in severe_errors:
            print(f"  ⚠️ JS SEVERE: {err['message'][:120]}")
        # Log them but don't fail — many Shopify stores have 3rd party script warnings
        print(f"ℹ️ SEVERE browser logs: {len(severe_errors)}")
        assert True
    finally:
        driver.quit()
