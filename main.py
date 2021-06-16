from selenium import webdriver
import time
from fake_useragent import UserAgent
from proxy import proxy_list
import random

ua = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={ua.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")
options.add_argument(f"--proxy-server={random.choice(proxy_list)}")

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://nvk209.kiev.ua/")
    link = driver.find_elements_by_xpath('//*[@id="meganavigator"]/li[4]/a')
    time.sleep(5)
    x = link[0].click()
    photo = driver.find_element_by_xpath('//*[@id="yt_component"]/div/div/p[1]/img').get_attribute("src")

    print(photo)
    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
