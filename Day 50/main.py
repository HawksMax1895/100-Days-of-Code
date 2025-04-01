from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
import dotenv
import time

dotenv.load_dotenv()

PHONE = os.environ.get("PHONE")

def wait_for_authentication(driver, timeout=1200):
    """Wait until the user is logged in by checking for a known post-login element."""
    print("Waiting for login (CAPTCHA and 2FA)...")
    try:
        # Wait for a known element that only shows up after successful login
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="q-1751151019"]/div/div[1]/div/div/div[3]/button[1]/div[2]/div[2]/div'))
        )
        print("Login successful!")
    except TimeoutException:
        print("Timeout waiting for login. Are you sure you completed CAPTCHA/2FA?")

URL = "https://tinder.com/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

login = driver.find_element(By.XPATH, '//*[@id="q-22769943"]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a/div[2]')
login.click()
time.sleep(1)

phone_login = driver.find_element(By.XPATH, '//*[@id="q-1751151019"]/div/div/div/div[1]/div/div/div[2]/div[2]/span/div[3]/button')
phone_login.click()
time.sleep(1)

phone_input = driver.find_element(By.ID, "phone_number")
phone_input.send_keys(PHONE, Keys.ENTER)

## Wait for CAPTCHA and 2 Factor Authentication is done and 
wait_for_authentication(driver)

clicked = False
for _ in range(5):
    try:
        allow.click()
        clicked = True
        break
    except ElementClickInterceptedException:
        print("Click blocked — retrying...")
        time.sleep(1)

if not clicked:
    raise Exception("Failed to click element after retries.")

allow_location = driver.find_element(By.XPATH, '//*[@id="q-1751151019"]/div/div[1]/div/div/div[3]/button[1]/div[2]/div[2]')
allow_location.click()
time.sleep(5)

while True:
    try:
        # ✅ Wait and click optional button if it appears (max wait 2s)
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="q-1751151019"]/div/div[1]/button[2]/div[2]/div[2]/div'))
        ).click()
        print("Clicked optional popup button.")
        time.sleep(1)
    except TimeoutException:
        pass  # It’s fine if the button didn’t show up

    try:
        # ✅ Wait until the "Like" button is clickable
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div/div/div/div[1]/div/div/div[4]/div/div[4]/button'))
        ).click()
        print("Liked!")
        time.sleep(1)
    except (TimeoutException, ElementClickInterceptedException) as e:
        print(f"Error while liking: {e}")
        time.sleep(1)
        continue  # You may want to retry instead of breaking

