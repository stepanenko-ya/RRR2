
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from fake_useragent import UserAgent
from proxy import proxy_list
import random
from selenium.webdriver.common.keys import Keys
import csv

ua = UserAgent()


def try_ip():
    x = True
    while x:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")
        options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
        print(random.choice(proxy_list))
        driver = webdriver.Chrome(options=options)
        try:
            driver.get("https://api.myip.com/")
            print(driver.find_element_by_tag_name("body").text)
            time.sleep(5)
        except Exception as ex:
            print(ex)
        else:
            x = False

        finally:
            driver.close()
            driver.quit()

try_ip()