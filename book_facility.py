"""
Automate ADDA facility booking exactly as recorded in seq_adda.io.seqe
--------------------------------------------------------------------
• Loads adda.io, clicks “Sign In”
• Enters email & password
• Navigates to Facilities tab
• Selects “Club House - Badminton Court 3”
• Picks tomorrow’s date
• Chooses slot 17:00-18:00
• Selects flat F3-402
• Clicks “Check Availability” (and optionally “Book Facility”)

Edit the constants in ALL_CAPS to change behaviour.
"""

from datetime import date, timedelta
import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# ------------------------------------------------------------------
# CONFIGURABLE CONSTANTS – edit only these
# ------------------------------------------------------------------
ADDA_EMAIL      = "kripajoym@gmail.com"
ADDA_PASSWORD   = "Adda@1234567"

FACILITY_NAME   = "Club House - Badminton Court 3"   # label from <select>
SLOT_TEXT       = "13:00:00 to 14:00:00"             # visible text in slot <select>
FLAT_TEXT       = "F3-402"                           # visible text in flat <select>

BOOK_FOR_TOMORROW = True      # True → selects tomorrow automatically
# ------------------------------------------------------------------

def launch_browser() -> "webdriver":
    opts = ChromeOptions()
    opts.add_argument("--start-maximized")
    # comment out headless if you prefer to see the browser while running
    opts.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=opts)

def wait(driver, locator, sec=15):
    """Shorthand for WebDriverWait"""
    return WebDriverWait(driver, sec).until(EC.presence_of_element_located(locator))

def main():
    driver = launch_browser()
    wait_for_click = WebDriverWait(driver, 15).until

    try:
        # --- 1. open adda.io & click “Sign In” -----------------------
        driver.get("https://adda.io")
        wait_for_click((By.LINK_TEXT, "Sign In")).click()

        # --- 2. log in ----------------------------------------------
