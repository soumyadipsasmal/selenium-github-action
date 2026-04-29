"""
browser_setup.py
────────────────
WebDriver factory for anvicouture.com tests.

Usage:
    from utils.browser_setup import BrowserSetup

    driver = BrowserSetup.get_driver()               # default Chrome headless
    driver = BrowserSetup.get_driver("chrome")       # headed Chrome
    driver = BrowserSetup.get_driver("mobile")       # mobile viewport
    driver = BrowserSetup.get_driver("tablet")       # tablet viewport
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

BASE_URL    = os.getenv("BASE_URL", "https://anvicouture.com")
HEADLESS    = os.getenv("HEADLESS", "true").lower() == "true"
PAGE_LOAD   = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
IMPLICIT_W  = int(os.getenv("IMPLICIT_WAIT", "0"))   # use explicit waits; keep 0


class BrowserSetup:
    """Factory that returns a configured Chrome WebDriver."""

    # ── Viewport presets ──────────────────────────────────────────────────
    VIEWPORTS = {
        "desktop": (1920, 1080),
        "laptop":  (1366, 768),
        "tablet":  (768,  1024),
        "mobile":  (390,  844),
    }

    @classmethod
    def get_driver(cls, profile: str = "desktop") -> webdriver.Chrome:
        """
        Return a Chrome driver for the given profile name.
        Profiles: 'desktop' | 'laptop' | 'tablet' | 'mobile'
        """
        width, height = cls.VIEWPORTS.get(profile, cls.VIEWPORTS["desktop"])
        options = cls._build_options(width, height)
        driver  = webdriver.Chrome(service=ChromeService(), options=options)
        cls._configure_driver(driver)
        return driver

    @classmethod
    def get_driver_custom(cls, width: int = 1920, height: int = 1080) -> webdriver.Chrome:
        """Return a Chrome driver with an arbitrary viewport size."""
        options = cls._build_options(width, height)
        driver  = webdriver.Chrome(service=ChromeService(), options=options)
        cls._configure_driver(driver)
        return driver

    # ── Private helpers ───────────────────────────────────────────────────
    @classmethod
    def _build_options(cls, width: int, height: int) -> ChromeOptions:
        options = ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")

        # Suppress 'Chrome is being controlled by automated software' banner
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Enable browser-level logging so tests can read console errors
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        return options

    @classmethod
    def _configure_driver(cls, driver: webdriver.Chrome):
        driver.set_page_load_timeout(PAGE_LOAD)
        if IMPLICIT_W:
            driver.implicitly_wait(IMPLICIT_W)
