from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#URL="https://en.wikipedia.org/wiki/Main_Page"
URL="http://secure-retreat-92358.herokuapp.com/"

# Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# no_articles = driver.find_element(By.XPATH, '//*[@id="articlecount"]/ul/li[2]/a[1]')
# print(no_articles.text)
#
# #no_articles.click()
#
# # all_portals = driver.find_element(By.LINK_TEXT, "Content portals")
# # all_portals.click()
#
# search = driver.find_element(By.NAME, "search")
# search.send_keys("Python", Keys.ENTER)

f_name = driver.find_element(By.NAME, "fName")
l_name = driver.find_element(By.NAME, "lName")
mail = driver.find_element(By.NAME, "email")

f_name.send_keys("Max")
l_name.send_keys("Radmacher")
mail.send_keys("maxradmacher@gmail.com", Keys.ENTER)


#driver.quit()