from bs4 import BeautifulSoup
from selenium import webdriver
import time
from fake_useragent import UserAgent
from proxy import proxy_list
import random
from selenium.webdriver.common.keys import Keys
import csv

ua = UserAgent()

URL = "https://www.iparts.pl/znajdz/?idCar=&query="


def writer(*args):
    result = "|".join(*args)
    with open("RESULT", "a+") as file:
        file.write(result + "\n")


def finder():
    with open('p.csv') as file:
        poland_items = [i.split("|") for i in file.readlines()]
    return poland_items







def iparts(findr):
    for el in findr:
        hunter_list = el[1:3]
        vendor = hunter_list[0]
        hunter_derty = " ".join(hunter_list)
        hunter = hunter_derty.replace(" ", "+").replace("/", "%")
        finder_url = URL + hunter
        del el[6:]
        x = True
        while x:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
            driver = webdriver.Chrome(options=options)
            link = None
            price = None
            try:
                driver.get(finder_url)
                items = driver.find_element_by_id('SklepKatalog').find_elements_by_class_name("produkt")
                if len(items) == 0:
                    link = "product not found"
                    price = 0
                else:
                    iter_items = iter(items)
                    for item in iter_items:
                        time.sleep(8)
                    # -------------------------------------------------------------------------------------------
                        name_item = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").text
                        if vendor in name_item.strip():
                            if hunter_list[1].upper() in name_item.upper():
                                item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").click()
                                time.sleep(8)
                                elements = driver.find_element_by_css_selector('span[itemprop="mpn"]').text.replace(" ", "")
                                if vendor.replace(" ", "") == elements:
                                    link = driver.current_url
                                    el.append(link)
                                    writer(el)
                                    break
                                else:
                                    driver.back()
                                    print("должно взять следующую карточку")
                     # -------------------------------------------------------------------------------------------------
                    else:
                        nastepna = driver.find_element_by_class_name("button-and-number-pager")
                        if nastepna:
                            next_page = nastepna.click()
                            print(driver.current_url)
                        else:
                            el.append("item is out")
                            el.append("0")
                            writer(el)
            except Exception as ex:
               print(ex)
            else:
                x = False
                el.append(link)
                el.append(price)
                writer(el)
            finally:
                driver.close()
                driver.quit()

if __name__ == "__main__":
    findr = finder()
    iparts(findr)



