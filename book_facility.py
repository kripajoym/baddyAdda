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
    # comment out headless=False if you prefer a visible browser
    opts.add_argument("--headless=new")
    return Chrome(ChromeDriverManager().install(), options=opts)

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
        wait(driver, (By.ID, "loginEmail")).send_keys(ADDA_EMAIL)
        driver.find_element(By.ID, "password").send_keys(ADDA_PASSWORD)
        driver.find_element(By.XPATH, "//button[.='Sign In']").click()

        # --- 3. land inside MyADDA, open Facilities tab -------------
        wait_for_click(
            (By.XPATH, "//span[normalize-space()='Facilities' or text()='Facilities']")
        ).click()

        # Facilities UI is an AngularJS SPA → switch to the iframe-less URL
        driver.get("https://in.adda.io/myadda/facilities-index.php#/facilities")
        wait(driver, (By.ID, "fac_name"))

        # --- 4. choose desired facility -----------------------------
        Select(driver.find_element(By.ID, "fac_name")).select_by_visible_text(FACILITY_NAME)

        # --- 5. pick booking date -----------------------------------
        if BOOK_FOR_TOMORROW:
            target_date = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")
            js = f"document.getElementById('datepicker').value = '{target_date}'"
            driver.execute_script(js)
        else:
            driver.find_element(By.ID, "datepicker").click()
            # – if not auto-filling, user must interact with date-picker here –

        # --- 6. select time slot ------------------------------------
        Select(driver.find_element(By.NAME, "fac_slot_id")).select_by_visible_text(SLOT_TEXT)

        # --- 7. select flat -----------------------------------------
        Select(driver.find_element(By.NAME, "flatId")).select_by_visible_text(FLAT_TEXT)

        # --- 8. check availability (and optionally book) ------------
        driver.find_element(By.XPATH, "//button[normalize-space()='Check Availability']").click()

        # wait for success OR error popup
        try:
            ok_btn = wait_for_click((By.XPATH, "//button[.='Book Facility']"), sec=8)
            print("✅ Slot available – booking now …")
            ok_btn.click()
            # brief wait for server confirmation
            time.sleep(2)
        except Exception:
            print("❌ Slot not available or booking restricted for today.")

    finally:
        # comment out if you want the browser left open
        driver.quit()

if __name__ == "__main__":
    main()
