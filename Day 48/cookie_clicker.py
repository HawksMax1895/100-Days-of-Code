from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

URL="https://orteil.dashnet.org/cookieclicker/"

# Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Wait until the cookie accept button is clickable and click it
try:
    # Wait max 10 seconds for the element to be present
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-cta-consent"))
    )
    cookie_button.click()
except Exception as e:
    print("Cookie button not found or already accepted:", e)

time.sleep(1)
language = driver.find_element(By.XPATH, '//*[@id="langSelect-EN"]')
language.click()

time.sleep(1)

#Site loaded up

buy_time = time.time() + 5
end_time = time.time() + 300


cookie = driver.find_element(By.XPATH, '//*[@id="bigCookie"]')

product_divs = driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")

while True:
    cookie.click()
    if time.time() > buy_time:
        # Get current cookie count
        money_str = driver.find_element(By.ID, "cookies").text.split()[0]
        money = int(money_str.replace(",", ""))

        # STEP 1: Try upgrades
        upgrade_divs = driver.find_elements(By.CSS_SELECTOR, "div.crate.upgrade.enabled")
        affordable_upgrades = {}

        for upgrade in upgrade_divs:
            # Hover to trigger tooltip
            ActionChains(driver).move_to_element(upgrade).perform()
            time.sleep(0.03)

            try:
                tooltip = driver.find_element(By.ID, "tooltip")
                tooltip_text = tooltip.text

                # Find first number (e.g. 600,000) and parse
                import re
                match = re.search(r'([\d,]+)', tooltip_text)
                if match:
                    price = int(match.group(1).replace(",", ""))
                    if price <= money:
                        affordable_upgrades[price] = upgrade
            except:
                continue  # In case tooltip fails

        # STEP 2: Buy most expensive affordable upgrade
        if affordable_upgrades:
            max_price = max(affordable_upgrades)
            affordable_upgrades[max_price].click()
            print(f"Bought upgrade for {max_price}")
        else:
            # STEP 3: Try products instead
            product_divs = driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")
            affordable_products = {}

            for product in product_divs:
                try:
                    price_text = product.find_element(By.CSS_SELECTOR, ".price").text.replace(",", "")
                    price = int(price_text)
                    if price <= money:
                        affordable_products[price] = product
                except:
                    continue

            if affordable_products:
                max_price = max(affordable_products)
                affordable_products[max_price].click()
                print(f"Bought product for {max_price}")

        buy_time += 5
    if time.time() > end_time:
        cps = driver.find_element(By.ID, "cookiesPerSecond").text
        print(f"🍪 Final cookies per second: {cps}")
        break
driver.quit()

