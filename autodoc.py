from selenium import webdriver
import time
from fake_useragent import UserAgent
from proxy import proxy_list
import random
from selenium.webdriver.common.keys import Keys

ua = UserAgent()


def finder():
    finders = []
    with open('poland.csv') as file:
        for i in file.readlines()[3:]:
            item_information = i.split("|")
            finders.append(f"{item_information[1]} {item_information[2]}")
    return finders


def autodoc(list_finders):
    for el in list_finders:
        x = True
        while x:
            print(f"finders element: {el}")
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--headless")
            options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
            driver = webdriver.Chrome(options=options)
            try:
                driver.get("https://www.autodoc.pl/")
                input = driver.find_element_by_id('search')
                input.clear()
                input.send_keys(f'{el}')
                driver.implicitly_wait(5)
                input.send_keys(Keys.ENTER)

                try:
                    container = driver.find_elements_by_class_name("cont")
                    url = container[0].find_element_by_class_name("description").find_element_by_class_name('ga-click').get_attribute("href")
                except:
                    url = "product is out of stock"
                try:
                    container = driver.find_elements_by_class_name("cont")
                    dirty_price = container[0].find_element_by_xpath('//*[@id="content"]/div[2]/div[5]/ul/li[1]/div[1]/div[4]/div[3]/p[2]').text
                    price = dirty_price.split(' ')[0]
                except:
                    price = "0"
                file_res = open('autodoc.csv', "a+")
                file_res.write(f"{url}|{price}\n")
                file_res.close()
            except Exception as ex:
                print(ex)
            else:
                x = False

            finally:
                driver.close()
                driver.quit()


if __name__ == "__main__":
    list_finders = finder()
    autodoc(list_finders[92:])
