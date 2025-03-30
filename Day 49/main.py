from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
import os
import dotenv
import time
import random

dotenv.load_dotenv()

MAIL = os.environ.get("MAIL")
PASSWORD = os.environ.get("PASSWORD")
URL = "https://www.linkedin.com/jobs/search/?currentJobId=4174319915&distance=25&geoId=100545973&keywords=projektmanager%20f%26e&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true"

# Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# Add this to avoid detection
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
# Mask selenium usage
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get(URL)


# Add random delays to appear more human-like
def random_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))


# Wait for initial page load
random_delay(2, 4)

# Handle login
try:
    login = driver.find_element(By.XPATH,
                                '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
    login.click()
    random_delay()

    login_mail = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_key"]')
    login_password = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_password"]')

    login_mail.send_keys(MAIL)
    login_password.send_keys(PASSWORD, Keys.ENTER)

    # Wait for login to complete - longer wait
    random_delay(3, 5)
    print("✅ Login erfolgreich")
except Exception as e:
    print(f"⚠️ Login-Prozess hatte ein Problem: {str(e)}")

wait = WebDriverWait(driver, 10)


def wait_until_overlay_is_gone(timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".artdeco-global-alert__action-wrapper,.artdeco-modal"))
        )
    except TimeoutException:
        print("⚠️ Overlay ist nicht verschwunden – versuche trotzdem")

    # Always add a short delay after checking for overlay
    time.sleep(0.5)


def click_safe(element, description=""):
    MAX_ATTEMPTS = 3
    attempt = 0

    while attempt < MAX_ATTEMPTS:
        try:
            attempt += 1
            wait_until_overlay_is_gone()
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable(element))
            element.click()
            print(f"✅ Klick auf {description} erfolgreich")
            return True
        except ElementClickInterceptedException:
            print(f"⚠️ Klick auf {description} wurde blockiert – Versuch {attempt}/{MAX_ATTEMPTS}")
            # Try to dismiss any dialogs
            try:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
            except:
                pass
        except Exception as e:
            print(f"⚠️ Problem beim Klicken auf {description}: {str(e)} – Versuch {attempt}/{MAX_ATTEMPTS}")
            time.sleep(1)

    print(f"❌ Konnte {description} nach {MAX_ATTEMPTS} Versuchen nicht klicken")
    return False


def try_click_follow():
    try:
        # Try multiple possible follow button selectors
        follow_selectors = [
            "//button[contains(text(), 'Follow')]",
            "//button[contains(@aria-label, 'Follow')]",
            "//button[contains(@class, 'follow')]"
        ]

        for selector in follow_selectors:
            try:
                follow_buttons = driver.find_elements(By.XPATH, selector)
                if follow_buttons:
                    for btn in follow_buttons:
                        if btn.is_displayed():
                            if click_safe(btn, "Follow Button"):
                                print("➕ Firma gefolgt")
                                return True
            except:
                continue

        print("ℹ️ Kein Follow-Button gefunden oder bereits gefolgt")
        return False
    except Exception as e:
        print(f"⚠️ Fehler beim Folgen: {str(e)}")
        return False


# Process jobs - improved with fresh elements on each job
num_jobs_to_process = 10  # You can adjust this number

# First, get the total count
try:
    print("🔍 Suche nach Jobs...")
    # Wait for job listings to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-card-container")))

    # Use a more reliable method to get job cards
    all_jobs = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
    job_count = min(len(all_jobs), num_jobs_to_process)
    print(f"📋 {job_count} Jobs werden verarbeitet")
except Exception as e:
    print(f"❌ Konnte keine Jobs finden: {str(e)}")
    job_count = 0

# Process each job with a fresh reference each time
for index in range(job_count):
    print(f"\n🔄 Verarbeite Job {index + 1}/{job_count}")
    try:
        # Get a fresh list of job elements each time to avoid stale references
        current_jobs = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
        if index >= len(current_jobs):
            print(f"⚠️ Nicht genug Jobs in der Liste, nur {len(current_jobs)} gefunden")
            break

        # Get the current job
        current_job = current_jobs[index]

        # Scroll to job card
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", current_job)
        random_delay(0.5, 1.5)

        # Click on job
        if not click_safe(current_job, f"Job #{index + 1}"):
            continue

        # Wait for job details to load
        random_delay(1, 2)

        # Try to find and click save button using multiple possible selectors
        try:
            save_selectors = [
                "//button[contains(@aria-label, 'Save')]",
                "//button[contains(@data-control-name, 'save')]",
                "//button[contains(@class, 'jobs-save-button')]",
                "//button[contains(@class, 'bookmark')]"
            ]

            save_button_found = False
            for selector in save_selectors:
                try:
                    save_buttons = driver.find_elements(By.XPATH, selector)
                    if save_buttons:
                        for btn in save_buttons:
                            if btn.is_displayed():
                                if click_safe(btn, "Save Button"):
                                    print("💾 Job gespeichert")
                                    save_button_found = True
                                    break
                        if save_button_found:
                            break
                except:
                    continue

            if not save_button_found:
                print("ℹ️ Kein Save-Button gefunden oder Job bereits gespeichert")
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern: {str(e)}")

        # Try to find and click company link
        try:
            random_delay(1, 2)

            # Try multiple possible company link selectors
            company_selectors = [
                "//a[contains(@data-control-name, 'company_link')]",
                "//a[contains(@class, 'company-link')]",
                "//a[contains(@href, '/company/')]"
            ]

            company_link_found = False
            for selector in company_selectors:
                try:
                    company_links = driver.find_elements(By.XPATH, selector)
                    if company_links:
                        for link in company_links:
                            if link.is_displayed():
                                if click_safe(link, "Firmenlink"):
                                    print("🏢 Zum Firmenprofil navigiert")
                                    company_link_found = True
                                    break
                        if company_link_found:
                            break
                except:
                    continue

            if company_link_found:
                # At company page, try to follow
                random_delay(1, 2)
                try_click_follow()

                # Go back to job listing
                driver.back()
                random_delay(2, 3)
            else:
                print("ℹ️ Kein Firmenlink gefunden")
        except Exception as e:
            print(f"⚠️ Fehler beim Firmenprofil: {str(e)}")
            # Try to get back to job listing
            try:
                driver.back()
                random_delay(2, 3)
            except:
                pass

    except WebDriverException as e:
        if "invalid session id" in str(e):
            print("❌ Browser-Session wurde unterbrochen. Skript wird beendet.")
            break
        print(f"❌ Fehler bei Job #{index + 1}: {str(e)}")

        # Try to go back to main job page if needed
        try:
            current_url = driver.current_url
            if "jobs/view" not in current_url and "jobs/search" not in current_url:
                print("⚠️ Navigation scheint falsch zu sein. Zurück zur Jobsuche...")
                driver.get(URL)
                random_delay(2, 3)
        except:
            # Last resort - go back to job search page
            try:
                driver.get(URL)
                random_delay(2, 3)
            except:
                pass
    except Exception as e:
        print(f"❌ Unerwarteter Fehler bei Job #{index + 1}: {str(e)}")

print("\n✅ Skript beendet")
# Don't close the browser at the end
# driver.quit()