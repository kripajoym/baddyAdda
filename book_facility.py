from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Open facility booking page
    driver.get('https://in.adda.io/myadda/facilities-index.php#/facilities')
    time.sleep(5)  # Allow page to load

    # 2. Log in
    driver.find_element(By.ID, 'inputEmail').send_keys('kripajoym@gmail.com')
    driver.find_element(By.ID, 'inputPassword').send_keys('Adda@1234567')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(7)  # Allow time for login and redirects

    # 3. Navigate and Book Facility
    # The following part MUST be updated with correct XPATH/CSS selectors for:
    #   - Selecting the facility
    #   - Setting the booking date/time
    #   - Confirming or submitting the booking

    # Example placeholders – update these!
    # driver.find_element(By.XPATH, 'REPLACE_WITH_FACILITY_XPATH').click()
    # time.sleep(3)
    # driver.find_element(By.XPATH, 'REPLACE_WITH_DATE_XPATH').send_keys('2024-06-25')
    # driver.find_element(By.XPATH, 'REPLACE_WITH_TIME_XPATH').send_keys('09:00')
    # driver.find_element(By.XPATH, 'REPLACE_WITH_BOOK_BUTTON_XPATH').click()
    # time.sleep(3)

    print("Booking attempted (verify selectors and booking logic).")

finally:
    driver.quit()
