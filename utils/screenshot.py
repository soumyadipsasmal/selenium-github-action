"""
screenshot.py
─────────────
Screenshot helpers for the Selenium test suite.

Usage:
    from utils.screenshot import take_screenshot, take_full_page_screenshot

    take_screenshot(driver, "login_page")
    take_screenshot(driver, "checkout", subfolder="cart")
    take_full_page_screenshot(driver, "full_homepage")
"""

import os
from datetime import datetime

SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")


def _build_path(name: str, subfolder: str = "") -> str:
    """Return a unique, timestamped file path under SCREENSHOT_DIR."""
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace("::", "_").replace("/", "_").replace(" ", "_")
    directory = os.path.join(SCREENSHOT_DIR, subfolder) if subfolder else SCREENSHOT_DIR
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, f"{safe_name}_{ts}.png")


def take_screenshot(driver, name: str, subfolder: str = "") -> str:
    """
    Save a viewport screenshot and return the file path.

    Args:
        driver:     Selenium WebDriver instance.
        name:       Base filename (timestamp appended automatically).
        subfolder:  Optional sub-directory inside screenshots/.
    """
    path = _build_path(name, subfolder)
    driver.save_screenshot(path)
    print(f"📸 Screenshot → {path}")
    return path


def take_full_page_screenshot(driver, name: str, subfolder: str = "") -> str:
    """
    Scroll-stitch a full-page screenshot via JS and return the file path.
    Falls back to a normal viewport screenshot if anything goes wrong.
    """
    path = _build_path(f"{name}_full", subfolder)
    try:
        original_size = driver.get_window_size()
        page_width    = driver.execute_script("return document.body.scrollWidth")
        page_height   = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(page_width, page_height)
        driver.save_screenshot(path)
        driver.set_window_size(original_size["width"], original_size["height"])
    except Exception:
        driver.save_screenshot(path)   # fallback
    print(f"📸 Full-page screenshot → {path}")
    return path


def take_failure_screenshot(driver, test_name: str) -> str:
    """
    Capture a screenshot prefixed with FAIL_ for easy filtering.
    Intended to be called inside a pytest fixture on test failure.
    """
    path = _build_path(f"FAIL_{test_name}", subfolder="failures")
    driver.save_screenshot(path)
    print(f"❌ Failure screenshot → {path}")
    return path


def clear_screenshots(subfolder: str = ""):
    """Delete all .png files from the screenshots directory (or a subfolder)."""
    directory = os.path.join(SCREENSHOT_DIR, subfolder) if subfolder else SCREENSHOT_DIR
    if not os.path.isdir(directory):
        return
    removed = 0
    for fname in os.listdir(directory):
        if fname.endswith(".png"):
            os.remove(os.path.join(directory, fname))
            removed += 1
    print(f"🗑️  Removed {removed} screenshot(s) from {directory}")
