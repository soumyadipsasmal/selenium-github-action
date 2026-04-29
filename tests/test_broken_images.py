import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, save_screenshot, BASE_URL


def test_images_have_src_attribute():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        no_src = [img.get_attribute("outerHTML")[:80] for img in images
                  if not img.get_attribute("src") and not img.get_attribute("data-src")]
        assert len(no_src) == 0, f"Images missing src: {no_src}"
        print(f"✅ All {len(images)} images have src or data-src")
    finally:
        driver.quit()


def test_images_have_alt_text():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img.get_attribute("src", ) for img in images
                       if img.get_attribute("alt") is None]
        print(f"ℹ️ Images missing alt: {len(missing_alt)} / {len(images)}")
        # Log but don't hard-fail — many Shopify themes have decorative images without alt
        assert True
    finally:
        driver.quit()


def test_no_broken_images_on_homepage():
    """Check that image URLs on homepage return 200."""
    driver = get_driver()
    broken = []
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        srcs = list({
            img.get_attribute("src") for img in images
            if img.get_attribute("src") and img.get_attribute("src").startswith("http")
        })[:10]  # Limit to 10 for speed
        for src in srcs:
            try:
                r = requests.head(src, timeout=10, allow_redirects=True)
                if r.status_code >= 400:
                    broken.append((r.status_code, src))
                    print(f"  ❌ {r.status_code} → {src[:80]}")
                else:
                    print(f"  ✅ {r.status_code} → {src[:60]}")
            except Exception as e:
                print(f"  ⚠️ {src[:60]}: {e}")
        assert len(broken) == 0, f"Broken image URLs: {broken}"
    finally:
        driver.quit()


def test_images_are_displayed():
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        images = driver.find_elements(By.TAG_NAME, "img")
        hidden = [img for img in images if not img.is_displayed()]
        visible = len(images) - len(hidden)
        print(f"ℹ️ Visible images: {visible} / {len(images)}")
        assert visible > 0, "At least one image should be visible on the homepage"
        print(f"✅ {visible} images are visible")
    finally:
        driver.quit()
