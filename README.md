# Selenium GitHub Actions — E2E Test Suite

> Automated end-to-end test framework for [anvicouture.com](https://anvicouture.com)  
> Built with **Selenium 4**, **pytest**, and **GitHub Actions CI/CD**

---

## 📌 Project Overview

This project demonstrates a production-grade UI automation framework targeting a live Shopify e-commerce store. It covers the full testing lifecycle — from writing maintainable Page Object Models to running tests automatically in the cloud via GitHub Actions.

**Application Under Test:** [https://anvicouture.com](https://anvicouture.com)  
**Tech Stack:** Python · Selenium 4 · pytest · GitHub Actions · Chrome WebDriver

---

## 🗂️ Project Structure

```
selenium-github-action/
│
├── .github/
│   └── workflows/
│       └── selenium.yml          # CI/CD pipeline — runs on every push & PR
│
├── tests/                        # All test cases (34 files)
│   ├── test_homepage.py          # Homepage load, title, images, HTTPS
│   ├── test_header.py            # Header logo, navigation, cart icon
│   ├── test_footer.py            # Footer links, copyright, scroll visibility
│   ├── test_menu.py              # Nav links, href validation, collections link
│   ├── test_login.py             # Login form, invalid credentials, error messages
│   ├── test_logout.py            # Logout redirect, unauthenticated access
│   ├── test_signup.py            # Registration form, empty submit, login link
│   ├── test_forgot_password.py   # Recover link, recover form email field
│   ├── test_product.py           # Product listing, images, links, detail page
│   ├── test_search.py            # Search by URL, empty query, no-results message
│   ├── test_filter.py            # Sort by price/date via URL params
│   ├── test_cart.py              # Cart page, empty state, cart.json endpoint
│   ├── test_remove_cart.py       # Remove button state, empty cart validation
│   ├── test_update_cart.py       # Quantity inputs, cart.json item count
│   ├── test_checkout.py          # Checkout redirect, button visibility, no 500
│   ├── test_coupon.py            # Discount field, cart/checkout validation
│   ├── test_wishlist.py          # Wishlist icon detection on homepage/product
│   ├── test_whatsapp.py          # WhatsApp button, link URL, contact methods
│   ├── test_popup.py             # Newsletter popup, close button, body access
│   ├── test_scroll.py            # Scroll to top/bottom/middle, page height
│   ├── test_broken_links.py      # Internal link HTTP status, JS console errors
│   ├── test_broken_images.py     # Image src, alt text, HTTP 200 validation
│   ├── test_load_speed.py        # Load time < 10s, Navigation Timing API
│   ├── test_mobile.py            # 390×844 iPhone viewport tests
│   ├── test_tablet.py            # 768×1024 iPad portrait & landscape
│   ├── test_cross_browser.py     # Chrome / Firefox / Edge / Safari user agents
│   ├── test_outofstock.py        # Sold Out badge, Add to Cart availability
│   ├── test_custom_page.py       # About, Contact, Privacy, Refund, 404 pages
│   ├── test_data_driven.py       # Parametrized — search terms, collections, viewports
│   ├── test_failure_screenshot.py# Auto screenshot capture on test failure
│   ├── test_logging.py           # File + console logging, browser console errors
│   ├── test_retry.py             # Retry logic on timeout, explicit wait fallback
│   ├── test_parallel.py          # Parallel-safe isolated tests (pytest-xdist ready)
│   ├── test_google.py            # Original homepage smoke test
│   └── _driver.py                # Shared driver factory used by all test files
│
├── pages/                        # Page Object Models (POM pattern)
│   ├── home_page.py              # HomePage — navigation, header, footer, links
│   ├── login_page.py             # LoginPage — form actions, error messages
│   ├── product_page.py           # ProductPage — listing, detail, add-to-cart
│   ├── cart_page.py              # CartPage — cart state, checkout, discount
│   └── search_page.py            # SearchPage — search via URL and form
│
├── utils/                        # Reusable utility modules
│   ├── browser_setup.py          # BrowserSetup factory — desktop/tablet/mobile profiles
│   ├── logger.py                 # Structured logger → console + timestamped log file
│   ├── screenshot.py             # Screenshot helpers — viewport, full-page, failure
│   └── helpers.py                # Waits, scrolls, link checker, performance, retry
│
├── screenshots/                  # Auto-saved screenshots (viewport & full-page)
├── reports/                      # HTML test reports + log files
│
├── .github/workflows/
│   └── selenium.yml              # GitHub Actions CI pipeline
├── requirements.txt              # All Python dependencies (pinned versions)
├── pytest.ini                    # pytest configuration
├── conftest.py                   # Shared fixtures & failure screenshot hook
├── .gitignore
└── README.md
```

---

## ✅ Test Coverage

| Area | Test File | Cases |
|---|---|---|
| Homepage | `test_homepage.py` | Load, title, images, links, HTTPS |
| Header & Footer | `test_header.py`, `test_footer.py` | Logo, nav, cart icon, copyright |
| Navigation Menu | `test_menu.py` | Links, hrefs, collections, home link |
| Authentication | `test_login.py`, `test_logout.py`, `test_signup.py` | Valid/invalid login, form fields, redirects |
| Password Recovery | `test_forgot_password.py` | Forgot link, recover form |
| Products | `test_product.py` | Listing, images, detail page, add to cart |
| Search | `test_search.py` | Keyword, empty, no results |
| Filters & Sort | `test_filter.py` | Price ASC/DESC, newest sort |
| Cart | `test_cart.py`, `test_remove_cart.py`, `test_update_cart.py` | Empty state, JSON API, quantity |
| Checkout | `test_checkout.py`, `test_coupon.py` | Redirect, button, discount field |
| Wishlist / WhatsApp | `test_wishlist.py`, `test_whatsapp.py` | Icon presence, link validation |
| UI Behaviour | `test_popup.py`, `test_scroll.py` | Popups, scroll positions |
| Link & Image QA | `test_broken_links.py`, `test_broken_images.py` | HTTP 200, alt text, src validation |
| Performance | `test_load_speed.py` | < 10s load, Navigation Timing API |
| Responsive | `test_mobile.py`, `test_tablet.py` | 390×844, 768×1024, 1024×768 |
| Cross-Browser | `test_cross_browser.py` | Chrome, Firefox, Edge, Safari UAs |
| Edge Cases | `test_outofstock.py`, `test_custom_page.py` | Sold out, 404, policy pages |
| Advanced | `test_data_driven.py`, `test_parallel.py`, `test_retry.py` | Parametrize, parallel, retry |
| Framework QA | `test_logging.py`, `test_failure_screenshot.py` | Logging setup, screenshot on fail |

**Total: 34 test files · 120+ test cases**

---

## 🏗️ Design Patterns

### Page Object Model (POM)
Every page is represented as a class with locators and actions separated from test logic. Tests stay clean and readable; if the UI changes, only the Page Object needs updating.

```python
# pages/login_page.py
class LoginPage:
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")

    def login(self, email, password):
        self.enter_email(email).enter_password(password).click_submit()

# tests/test_login.py
def test_invalid_login(driver):
    page = LoginPage(driver)
    page.open().login("wrong@email.com", "badpassword")
    assert page.is_error_shown()
```

### Utility Layer
| Module | Responsibility |
|---|---|
| `BrowserSetup` | Single driver factory — one line to get Chrome for any viewport |
| `get_logger()` | Named loggers writing to console + `reports/test_run_<timestamp>.log` |
| `take_screenshot()` | Auto-timestamped, auto-named, sorted into subfolders |
| `helpers.py` | `retry()`, `wait_for_url_contains()`, `get_broken_links()`, `get_page_performance()` |

---

## ⚙️ GitHub Actions CI Pipeline

```yaml
# Triggers
on:
  push:            # Every push to main/develop
  pull_request:    # Every PR targeting main
  schedule:        # Daily at 06:00 UTC
  workflow_dispatch: # Manual trigger from GitHub UI
```

**What the pipeline does:**
1. Checks out code and sets up Python 3.11
2. Installs all dependencies from `requirements.txt`
3. Sets up Chrome (stable) and ChromeDriver
4. Runs the full test suite in `--headless=new` mode
5. Uploads the HTML report as an artifact (retained 30 days)
6. Uploads failure screenshots as a separate artifact (retained 7 days)

**Artifacts produced per run:**

| Artifact | When | Retention |
|---|---|---|
| `test-report-<run>` | Always | 30 days |
| `failure-screenshots-<run>` | On failure only | 7 days |

---

## 🚀 Local Setup & Running

### Prerequisites
- Python 3.11+
- Google Chrome (stable)

### Installation

```bash
git clone https://github.com/your-username/selenium-github-action.git
cd selenium-github-action
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with visible browser (headed mode)
HEADLESS=false pytest tests/ -v -s

# Run a specific file
pytest tests/test_login.py -v -s

# Run by keyword
pytest tests/ -k "cart or checkout" -v

# Run in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest tests/ -n auto
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://anvicouture.com` | Target URL |
| `HEADLESS` | `true` | Run Chrome headless |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout in seconds |
| `LOG_LEVEL` | `INFO` | Logging level |
| `SCREENSHOT_DIR` | `screenshots` | Screenshot output folder |
| `LOG_DIR` | `reports` | Log file output folder |

---

## 📊 Test Report

After every run an HTML report is generated at `reports/report.html`.

```bash
# Open after local run
open reports/report.html          # macOS
xdg-open reports/report.html      # Linux
```

On GitHub Actions, download it from the **Actions → run → Artifacts** section.

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11 | Language |
| Selenium | 4.43.0 | Browser automation |
| pytest | 9.0.3 | Test runner |
| pytest-html | 4.2.0 | HTML reports |
| requests | 2.33.1 | HTTP link checking |
| python-dotenv | 1.2.2 | Environment variables |
| GitHub Actions | — | CI/CD pipeline |
| Chrome | Stable | Browser under test |

---

## 👤 Author

**Soumya**  
QA Automation Engineer  
[GitHub](https://github.com/soumyadipsasmal) · [LinkedIn](https://www.linkedin.com/in/soumyadip-sasmal-479487243/)

---

> *This project was built to demonstrate real-world Selenium automation skills including Page Object Model design, CI/CD integration, responsive testing, and production-grade framework architecture.*
