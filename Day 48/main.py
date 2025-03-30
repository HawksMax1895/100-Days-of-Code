from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.python.org/")

# event_time = driver.find_element(By.XPATH, value='//*[@id="content"]/div/section/div[3]/div[2]/div/ul/li[1]/time')
event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget .menu li time")
event_titles = driver.find_elements(By.CSS_SELECTOR, ".event-widget .menu li a")

events = {time.text: title.text for title, time in zip(event_titles, event_times)}
print(events)

#driver.close()
driver.quit()
