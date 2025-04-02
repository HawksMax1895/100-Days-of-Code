import os
import dotenv
import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dotenv.load_dotenv()

PROMISED_DOWN = int(os.getenv("PROMISED_DOWN"))
PROMISED_UP = int(os.getenv("PROMISED_UP"))
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")    
URL_TWITTER = "https://x.com/"
URL_SPEEDTEST = "https://www.speedtest.net/"

class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

        self.up = 0
        self.down = 0

        self.driver.get(URL_SPEEDTEST)
        time.sleep(1)

        try:
            accept = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept.click()
        except Exception as e:
            print("Cookie-Banner wurde nicht gefunden oder bereits akzeptiert.")

        self.wait = WebDriverWait(self.driver, 60)

    def get_internet_speed(self):
        start = self.driver.find_element(By.CLASS_NAME, "js-start-test")
        start.click()
        #time.sleep(60)

        # Warte auf Download-Speed Ergebnis
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/div[3]/div/div[3]/div/div/div[2]/div[4]/div/div/div[2]/div/div/ul[1]'))
        )

        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text

        print(f"Download: {self.down} Mbps")
        print(f"Upload: {self.up} Mbps")

        return self.down, self.up


    def tweet_at_provider(self):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")

        self.driver = uc.Chrome(options=options)
        
        self.driver.get(URL_TWITTER)
        time.sleep(3)

        login = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[3]/a/div')
        login.click()
        time.sleep(3)
        
        input_usermame = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
        input_usermame.send_keys(TWITTER_EMAIL, Keys.ENTER)
        time.sleep(3)

        input_password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        input_password.send_keys(TWITTER_PASSWORD, Keys.ENTER)


        input("🚀 Script done. Press Enter to exit and close browser manually...")
        


bot = InternetSpeedTwitterBot()
#bot.get_internet_speed()
#print(bot.down)
#print(bot.up)
bot.tweet_at_provider()
        

