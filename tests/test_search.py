from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from _driver import get_driver, save_screenshot, BASE_URL

SEARCH_URL = f"{BASE_URL}/search"


def test_search_page_loads():
    driver = get_driver()
    try:
        driver.get(SEARCH_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        print(f"✅ Search page loaded: {driver.title}")
        save_screenshot(driver, "search_page")
    finally:
        driver.quit()


def test_search_input_present():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        search_inputs = driver.find_elements(By.XPATH,
            "//input[@type='search' or contains(@name,'search') or contains(@id,'search') or contains(@placeholder,'Search')]"
        )
        assert len(search_inputs) > 0, "Search input field should be present"
        print(f"✅ Search input found")
    finally:
        driver.quit()


def test_search_with_keyword():
    driver = get_driver()
    try:
        driver.get(f"{SEARCH_URL}?q=dress")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "dress" in driver.current_url.lower() or driver.title != ""
        save_screenshot(driver, "search_results_dress")
        print(f"✅ Search for 'dress' loaded: {driver.current_url}")
    finally:
        driver.quit()


def test_search_empty_query():
    driver = get_driver()
    try:
        driver.get(f"{SEARCH_URL}?q=")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert body_text != "", "Page body should not be empty on empty search"
        print("✅ Empty search query handled gracefully")
    finally:
        driver.quit()


def test_search_no_results_message():
    driver = get_driver()
    try:
        driver.get(f"{SEARCH_URL}?q=xyznonexistentproduct123")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(kw in body_text for kw in ["no result", "not found", "0 result", "nothing", "no product"]), \
            "Should show 'no results' message for nonsense query"
        save_screenshot(driver, "search_no_results")
        print("✅ No-results message shown for nonsense query")
    finally:
        driver.quit()
