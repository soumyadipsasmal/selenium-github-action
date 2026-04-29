"""
logger.py
─────────
Centralised logging for the Selenium test suite.

Usage:
    from utils.logger import get_logger

    log = get_logger(__name__)
    log.info("Page loaded")
    log.warning("Slow response")
    log.error("Element not found")
"""

import logging
import os
from datetime import datetime

LOG_DIR   = os.getenv("LOG_DIR", "reports")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# One timestamped log file per test session
_session_ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
_log_file    = os.path.join(LOG_DIR, f"test_run_{_session_ts}.log")
_initialized = False


def _init_root_logger():
    global _initialized
    if _initialized:
        return
    _initialized = True

    os.makedirs(LOG_DIR, exist_ok=True)

    fmt = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)-8s]  %(name)s  —  %(message)s",
        datefmt="%H:%M:%S",
    )

    # Console handler
    console_h = logging.StreamHandler()
    console_h.setFormatter(fmt)
    console_h.setLevel(LOG_LEVEL)

    # File handler
    file_h = logging.FileHandler(_log_file, encoding="utf-8")
    file_h.setFormatter(fmt)
    file_h.setLevel(logging.DEBUG)   # always capture DEBUG in file

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console_h)
    root.addHandler(file_h)


def get_logger(name: str = "selenium_tests") -> logging.Logger:
    """Return a named logger. Initialises root handlers on first call."""
    _init_root_logger()
    return logging.getLogger(name)


def log_step(logger: logging.Logger, step: str):
    """Log a clearly visible test-step banner."""
    logger.info(f"{'─' * 10}  STEP: {step}  {'─' * 10}")


def log_page_info(logger: logging.Logger, driver):
    """Log current URL and title — useful after every navigation."""
    logger.info(f"URL   : {driver.current_url}")
    logger.info(f"Title : {driver.title!r}")


def log_browser_errors(logger: logging.Logger, driver):
    """Pull SEVERE browser console logs and emit as warnings."""
    try:
        logs = driver.get_log("browser")
        severe = [e for e in logs if e.get("level") == "SEVERE"]
        if severe:
            for entry in severe:
                logger.warning(f"BROWSER SEVERE → {entry['message'][:140]}")
        else:
            logger.debug("No SEVERE browser console errors")
    except Exception as exc:
        logger.debug(f"Could not read browser logs: {exc}")
