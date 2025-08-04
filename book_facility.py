"""
Automate ADDA facility booking exactly as recorded in seq_adda.io.seqe
--------------------------------------------------------------------
• Loads adda.io, clicks “Sign In”
• Enters email & password
• Navigates to Facilities tab
• Selects “Club House - Badminton Court 3”
• Picks tomorrow’s date
• Chooses slot 13:00-14:00
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
    # Uncomment next line to run in headless mode once debugging is done
    # opts.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=opts)

def debug_page_state(driver, step_desc):
    print(f"[DEBUG] Step: {step_desc}")
    print(f"[DEBUG] Current URL: {driver.current_url}")
    print(f"[DEBUG] Page title: {driver.title}")
    try:
        snippet = driver.page_source[:500]
        print(f"[DEBUG] Page source snippet (first 500 chars): {snippet}")
    except Exception as e:
        print(f"[DEBUG] Could not get page source snippet: {e}")

def wait_for_presence_and_click(driver, locator, timeout=30, step_desc=""):
    debug_page_state(driver, step_desc)
    print(f"[DEBUG] Waiting for presence of element: {locator}")
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    element = driver.find_element(*locator)
    print(f"[DEBUG] Found element, clicking: {locator}")
    element.click()
    print(f"[DEBUG] Clicked element: {locator}")

def wait_for_presence(driver, locator, timeout=30, step_desc=""):
    debug_page_state(driver, step_desc)
    print(f"[DEBUG] Waiting for presence of element: {locator}")
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    print(f"[DEBUG] Element present: {locator}")
    return element

def close_cookies_banner(driver):
    try:
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
        )
        consent_button.click()
        print("[DEBUG] Closed cookie consent banner")
        time.sleep(1)
    except Exception:
        print("[DEBUG] No cookie consent banner present or already closed")

def main():
    driver = launch_browser()

    try:
        # --- 1. open adda.io and close cookie banner ----------------
        driver.get("https://adda.io")
        print("[DEBUG] Opened adda.io")
        time.sleep(4)
        close_cookies_banner(driver)

        # --- 2. click Sign In ----------------------------------------
        wait_for_presence_and_click(driver, (By.XPATH, "//*[contains(text(), 'Sign In')]"),
                                   step_desc="Clicking Sign In link")

        # --- 3. login -----------------------------------------------
        wait_for_presence(driver, (By.ID, "loginEmail"), step_desc="Waiting for login email input").send_keys(ADDA_EMAIL)
        driver.find_element(By.ID, "password").send_keys(ADDA_PASSWORD)
        driver.find_element(By.XPATH, "//button[.='Sign In']").click()
        print("[DEBUG] Submitted login form")
        time.sleep(3)

        # --- 4. open Facilities tab ---------------------------------
        wait_for_presence_and_click(driver,
            (By.XPATH, "//span[normalize-space()='Facilities' or text()='Facilities']"),
            step_desc="Clicking Facilities tab"
        )

        # Switch to iframe-less facilities page URL
        driver.get("https://in.adda.io/myadda/facilities-index.php#/facilities")
        wait_for_presence(driver, (By.ID, "fac_name"), step_desc="Waiting for facilities page")

        # --- 5. select facility -------------------------------------
        Select(driver.find_element(By.ID, "fac_name")).select_by_visible_text(FACILITY_NAME)
        print(f"[DEBUG] Selected facility: {FACILITY_NAME}")

        # --- 6. select booking date ---------------------------------
        if BOOK_FOR_TOMORROW:
            target_date = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")
            js = f"document.getElementById('datepicker').value = '{target_date}'"
            driver.execute_script(js)
            print(f"[DEBUG] Set booking date to: {target_date}")
        else:
            driver.find_element(By.ID, "datepicker").click()
            print("[DEBUG] Please interact with date picker manually (BOOK_FOR_TOMORROW=False)")

        # --- 7. select time slot -----------------------------------
        Select(driver.find_element(By.NAME, "fac_slot_id")).select_by_visible_text(SLOT_TEXT)
        print(f"[DEBUG] Selected time slot: {SLOT_TEXT}")

        # --- 8. select flat ----------------------------------------
        Select(driver.find_element(By.NAME, "flatId")).select_by_visible_text(FLAT_TEXT)
        print(f"[DEBUG] Selected flat: {FLAT_TEXT}")

        # --- 9. check availability and optionally book -------------
        driver.find_element(By.XPATH, "//button[normalize-space()='Check Availability']").click()
        print("[DEBUG] Clicked 'Check Availability' button")

        try:
            ok_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.='Book Facility']"))
            )
            print("✅ Slot available – booking now …")
            ok_btn.click()
            time.sleep(2)
        except Exception:
            print("❌ Slot not available or booking restricted for today.")

    finally:
        driver.quit()
        print("[DEBUG] Browser closed")

if __name__ == "__main__":
    main()
