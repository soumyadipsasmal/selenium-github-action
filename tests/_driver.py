"""Shared Chrome driver factory — imported by every test file."""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://anvicouture.com"


def get_driver(width=1920, height=1080):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)
    return driver


def save_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    path = f"screenshots/{name}.png"
    driver.save_screenshot(path)
    print(f"📸 Screenshot → {path}")
