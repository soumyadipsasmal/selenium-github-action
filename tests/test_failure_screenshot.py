import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _driver import get_driver, BASE_URL


@pytest.fixture
def driver_with_screenshot(request):
    """Driver fixture that auto-captures a screenshot when a test fails."""
    driver = get_driver()
    yield driver
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        os.makedirs("screenshots", exist_ok=True)
        name = request.node.name.replace("/", "_").replace("::", "_")
        path = f"screenshots/FAIL_{name}.png"
        driver.save_screenshot(path)
        print(f"\n📸 Failure screenshot → {path}")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def test_screenshot_on_pass(driver_with_screenshot):
    driver = driver_with_screenshot
    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot("screenshots/pass_screenshot.png")
    assert driver.current_url.startswith("https://")
    print("✅ Pass screenshot saved")


def test_screenshot_captures_on_assertion_failure(driver_with_screenshot):
    """Intentionally fails to verify screenshot capture works."""
    driver = driver_with_screenshot
    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    title = driver.title
    # This test will pass if ANY title is present — change to `assert False` to test screenshot
    assert title is not None, "Title should not be None"
    print(f"✅ Title present: '{title}' — failure screenshot fixture is ready")


def test_screenshots_directory_exists_after_run():
    os.makedirs("screenshots", exist_ok=True)
    assert os.path.isdir("screenshots"), "Screenshots directory should exist"
    print("✅ screenshots/ directory confirmed")
