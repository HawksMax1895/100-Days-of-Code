from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
import re

URL = "https://orteil.dashnet.org/cookieclicker/"

# Chrome Setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Cookie Consent
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-cta-consent"))
    )
    cookie_button.click()
except Exception as e:
    print("Cookie consent not found or already accepted:", e)

# Language selection
time.sleep(1)
driver.find_element(By.ID, "langSelect-EN").click()
time.sleep(2)

cookie = driver.find_element(By.ID, "bigCookie")

buy_time = time.time() + 5
end_time = time.time() + 300

while True:
    cookie.click()

    if time.time() > buy_time:
        # Aktuellen Cookie-Bestand ermitteln
        money_str = driver.find_element(By.ID, "cookies").text.split()[0]
        money = int(money_str.replace(",", ""))

        # === 1. Upgrades kaufen ===
        affordable_upgrades = {}
        upgrades = driver.find_elements(By.CSS_SELECTOR, "div.crate.upgrade.enabled")

        for upgrade in upgrades:
            try:
                ActionChains(driver).move_to_element(upgrade).perform()
                time.sleep(0.05)
                tooltip = driver.find_element(By.ID, "tooltip")
                match = re.search(r"([\d,]+)", tooltip.text)
                if match:
                    price = int(match.group(1).replace(",", ""))
                    if price <= money:
                        affordable_upgrades[price] = upgrade
            except Exception:
                continue

        if affordable_upgrades:
            try:
                max_price = max(affordable_upgrades)
                affordable_upgrades[max_price].click()
                print(f"✅ Bought upgrade for {max_price}")
            except StaleElementReferenceException:
                print("⚠️ Upgrade element was stale. Skipping.")
        else:
            # === 2. Produkte kaufen ===
            affordable_products = {}
            products = driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")

            for product in products:
                try:
                    price_text = product.find_element(By.CSS_SELECTOR, ".price").text
                    price = int(price_text.replace(",", ""))
                    if price <= money:
                        affordable_products[price] = product
                except Exception:
                    continue

            if affordable_products:
                try:
                    max_price = max(affordable_products)
                    affordable_products[max_price].click()
                    print(f"✅ Bought product for {max_price}")
                except StaleElementReferenceException:
                    print("⚠️ Product element was stale. Skipping.")

        buy_time += 5

    if time.time() > end_time:
        try:
            cps = driver.find_element(By.ID, "cookiesPerSecond").text
            print(f"\n🍪 Final cookies per second: {cps}")
        except Exception as e:
            print("❌ Couldn't read cookies per second:", e)
        break

driver.quit()
