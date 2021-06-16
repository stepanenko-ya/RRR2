from selenium import webdriver
import time
from fake_useragent import UserAgent
# from proxy import proxy_list
import random
from selenium.webdriver.common.keys import Keys
import csv
from multiprocessing import Pool

ua = UserAgent()

proxy_list = ['128.199.201.245:8080', '157.230.103.189:45153', '138.199.4.96:3128',
              '186.225.46.89:8080', '14.241.111.38:8080', '35.195.6.233:3128',
              '216.108.228.69:3128']
def finder():
    poland_items = []
    with open('p.csv') as file:
        for y, i in enumerate(file.readlines(), 1):
            lst = i.split("|")
            lst.insert(0, str(y))
            poland_items.append(lst)

    return poland_items


def writer(res_list):
    file = open("AAA.csv", "a+")
    writer = csv.writer(file, delimiter="|")
    writer.writerow(res_list)
    file.close()


def czesciauto(list_finders):
    counter = list_finders[0]
    finder_code = list_finders[2]
    brand_name = list_finders[3]
    hunter = " ".join([finder_code, brand_name])
    del list_finders[7:]

    x = True
    while x:
        print(counter)
        print(hunter)
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")
        options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get("https://www.czesciauto24.pl/")
            input = driver.find_element_by_id('search')
            input.clear()
            input.send_keys(f'{hunter}')
            driver.implicitly_wait(2)

            input.send_keys(Keys.ENTER)
            containers = driver.find_elements_by_class_name('brand-products')
            price = ""
            link = ""
            if len(containers) == 0:
                link = "product is out of stock"
                price = "0"
            else:
                finders = finder_code.upper().replace(" ", '')
                link = 'no such item'
                price = '0'
                for cont in containers:
                    vendor_code = cont.find_element_by_class_name('nr').find_element_by_tag_name("span").text.split(":")[1].replace(" ", "")
                    print(vendor_code)
                    if finders.strip() == vendor_code.strip():
                        name = cont.find_element_by_class_name("description").find_element_by_class_name("ga-click").text
                        print(name)
                        if brand_name.upper().strip() in name.upper().strip():
                            url = cont.find_element_by_class_name("description").find_element_by_class_name("ga-click").get_attribute("href")
                            dirty_price = cont.find_element_by_class_name("right_side").find_element_by_class_name("price").text
                            price = dirty_price.split(" ")[0]
                            if url:
                                link = url


        except Exception as ex:
            print(ex)
        else:
            x = False
            list_finders.append(link)
            list_finders.append(price)
            writer(list_finders)
        finally:
            driver.close()
            driver.quit()



if __name__ == "__main__":
    list_finders = finder()
    p = Pool(processes=1)
    p.map(czesciauto, list_finders)


