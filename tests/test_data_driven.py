import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL

# ── Data sets ──────────────────────────────────────────────────────────────
SEARCH_TERMS = ["dress", "kurti", "saree", "lehenga", "suit"]

COLLECTION_SLUGS = ["all", "new-arrivals", "sale", "festive", "bridal"]

VIEWPORTS = [
    ("desktop", 1920, 1080),
    ("laptop",  1366, 768),
    ("tablet",  768,  1024),
    ("mobile",  390,  844),
]


# ── Tests ──────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("term", SEARCH_TERMS)
def test_search_term(term):
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/search?q={term}")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, f"data_search_{term}")
        print(f"✅ Search '{term}' → {driver.current_url}")
    finally:
        driver.quit()


@pytest.mark.parametrize("slug", COLLECTION_SLUGS)
def test_collection_page(slug):
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/collections/{slug}")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert driver.current_url != ""
        save_screenshot(driver, f"data_collection_{slug}")
        print(f"✅ /collections/{slug} → {driver.current_url}")
    finally:
        driver.quit()


@pytest.mark.parametrize("name,width,height", VIEWPORTS)
def test_viewport_rendering(name, width, height):
    driver = get_driver(width=width, height=height)
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        vp = driver.execute_script("return {w: window.innerWidth, h: window.innerHeight};")
        save_screenshot(driver, f"data_viewport_{name}")
        assert vp["w"] > 0
        print(f"✅ {name} ({width}x{height}) → actual {vp['w']}x{vp['h']}")
    finally:
        driver.quit()
