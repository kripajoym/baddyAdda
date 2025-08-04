from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Open the facility booking website
    driver.get('https://in.adda.io/myadda/facilities-index.php#/facilities')
    time.sleep(5)  # wait for page/form to load

    # 2. Log in (update selectors as per login form)
    driver.find_element(By.ID, 'inputEmail').send_keys('YOUR_EMAIL')
    driver.find_element(By.ID, 'inputPassword').send_keys('YOUR_PASSWORD')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)

    # 3. Navigate to booking section (update steps as required)
    # Example: click facility, select date/time, fill form
    # The exact selectors must be updated after inspecting the site
    
    # driver.find_element(By.XPATH, 'XPATH_TO_FACILITY').click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, 'XPATH_TO_DATE_PICKER').send_keys('YYYY-MM-DD')
    # driver.find_element(By.XPATH, 'XPATH_TO_TIME_PICKER').send_keys('HH:MM')
    # driver.find_element(By.XPATH, '//button[text()="Book"]').click()
    # time.sleep(3)
    
    print("Booking attempted.")

finally:
    driver.quit()
