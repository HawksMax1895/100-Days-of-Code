from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import os
import dotenv
import time
import random

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

URL = "https://tinder.com/app/recs"

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


driver = webdriver.Chrome(options=chrome_options)

driver.get(URL)

print(driver.title)

# login = driver.find_element(By.XPATH, '//*[@id="q-22769943"]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a/div[2]')
# login.click()
# time.sleep(1)

# phone_login = driver.find_element(By.XPATH, '//*[@id="q-1751151019"]/div/div/div/div[1]/div/div/div[2]/div[2]/span/div[3]/button')
# phone_login.click()
# time.sleep(1)

# phone_input = driver.find_element(By.ID, "phone_number")
# phone_input.send_keys(PHONE, Keys.ENTER)

# ## Wait for CAPTCHA and 2 Factor Authentication is done and 
# wait_for_authentication(driver)

# clicked = False
# for _ in range(5):
#     try:
#         allow.click()
#         clicked = True
#         break
#     except ElementClickInterceptedException:
#         print("Click blocked — retrying...")
#         time.sleep(1)

# if not clicked:
#     raise Exception("Failed to click element after retries.")

# allow_location = driver.find_element(By.XPATH, '//*[@id="q-1751151019"]/div/div[1]/div/div/div[3]/button[1]/div[2]/div[2]')
# allow_location.click()
# time.sleep(5)

# Multiple possible XPaths for popup buttons
POPUP_XPATHS = [
    '//*[@id="q-1751151019"]/div/div[1]/button[2]/div[2]/div[2]/div',
    '//div[contains(@class, "modal")]//button[2]',
    '//button[contains(text(), "Not interested")]',
    '//button[contains(text(), "Maybe later")]',
    '//button[contains(text(), "No thanks")]',
    '//button[contains(text(), "Skip")]',
    '//button[contains(text(), "Continue")]'
]

# Multiple possible XPaths for like buttons - more comprehensive
LIKE_XPATHS = [
    '//*[@id="main-content"]/div[1]/div/div/div/div[1]/div/div/div[4]/div/div[4]/button',
    '//button[@aria-label="Like"]',
    '//button[contains(@aria-label, "Like")]',
    '//div[contains(@class, "Pos(r)")]/div/div/div/div[contains(@class, "Bgc")]/div/div[4]/button',
    '//span[text()="Like"]/parent::button',
    '//button[@data-testid="gamepad-like"]',
    '//div[@class="Mx(a) Fxs(0) Sq(70px) Sq(60px)--s"]/button',
    '//div[contains(@class, "CenterAlign")]/div/div[4]/button',
    '//div[contains(@class, "button")]/span[contains(text(), "Like")]/ancestor::button'
]

like_count = 0
start_time = time.time()
last_successful_xpath = None
error_count = 0
max_consecutive_errors = 5

def wait_for_profile_change(driver, timeout=3):
    """Wait for profile to change after liking"""
    try:
        time.sleep(0.5)  # Small initial delay for animation
        # This is a generic check for DOM changes - might need adjustment
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    except:
        pass  # Continue even if we can't detect a clear change

while True:
    # Handle popups
    for popup_xpath in POPUP_XPATHS:
        try:
            popup_button = WebDriverWait(driver, 0.3).until(
                EC.element_to_be_clickable((By.XPATH, popup_xpath))
            )
            popup_button.click()
            print("Dismissed popup")
            time.sleep(0.2)
            break
        except:
            continue
    
    # Try to like - prioritize last successful XPath if available
    liked = False
    
    # First try the last successful xpath if we have one
    if last_successful_xpath:
        try:
            like_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, last_successful_xpath))
            )
            like_button.click()
            like_count += 1
            elapsed_time = time.time() - start_time
            likes_per_minute = like_count / (elapsed_time / 60) if elapsed_time > 0 else 0
            print(f"Liked! Total: {like_count} | Rate: {likes_per_minute:.1f} likes/min")
            wait_for_profile_change(driver)
            time.sleep(random.uniform(0.3, 0.6))
            liked = True
            error_count = 0
        except:
            # If last successful xpath fails, clear it and try others
            last_successful_xpath = None
    
    # If last successful xpath failed, try all others
    if not liked:
        for like_xpath in LIKE_XPATHS:
            try:
                like_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, like_xpath))
                )
                
                time.sleep(random.uniform(0.1, 0.2))
                
                like_button.click()
                like_count += 1
                
                elapsed_time = time.time() - start_time
                likes_per_minute = like_count / (elapsed_time / 60) if elapsed_time > 0 else 0
                print(f"Liked! Total: {like_count} | Rate: {likes_per_minute:.1f} likes/min")
                
                # Remember this successful xpath
                last_successful_xpath = like_xpath
                
                # Wait for next profile to load
                wait_for_profile_change(driver)
                
                time.sleep(random.uniform(0.3, 0.6))
                
                liked = True
                error_count = 0
                break
                
            except Exception as e:
                continue
    
    # If all like attempts failed
    if not liked:
        error_count += 1
        print(f"Like button not found. Retry {error_count}/{max_consecutive_errors}...")
        
        # Add alternative fallback strategy - just try to click where the like button should be
        if error_count >= 3:
            try:
                # Try to click approximately where the like button should be
                print("Trying fallback click strategy...")
                driver.execute_script("""
                    // Try to find elements that might be related to buttons
                    let buttons = document.querySelectorAll('button');
                    // Click the 4th button if it exists (often the like button)
                    if (buttons.length >= 4) {
                        buttons[3].click();
                    }
                """)
                time.sleep(1)
                like_count += 1
                print(f"Tried fallback click. Total: {like_count}")
                error_count = 0
            except:
                pass
        
        # Stop if too many consecutive errors
        if error_count >= max_consecutive_errors:
            print(f"Too many consecutive errors ({max_consecutive_errors}). Stopping.")
            break
            
        time.sleep(1.5)  # Slightly longer wait when having issues