from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome("/Users/josephtang/PycharmProjects/FirstSeleniumTest/drivers/chromedriver")
driver.get("https://www.barcodelookup.com/")
time.sleep(15)
driver.find_element_by_name("search-input").send_keys("soda can" + Keys.ENTER)
current_url = driver.current_url
#time.sleep(10)

dict_of_everything = {} #key = barcode, values = list[item name, item category]

for page_num in range(2,500):
        ids = driver.find_elements_by_xpath("//*[@class = 'product-search-item']")
        item_names = [] # holds all the href values for each item
        for i in ids:
            item_names.append(i.get_attribute("href"))

        for i in item_names: #traverse through list of href values
            try:
                specific_name = driver.find_elements_by_xpath("//*[@href = '" + i + "']/li/div[2]/p[1]") #to get item names
                barcode = driver.find_elements_by_xpath("//*[@href = '" + i + "']/li/div[2]/p[2]") #to get barcode numbers
                item_category = driver.find_elements_by_xpath("//*[@href = '" + i + "']/li/div[2]/p[3]") # to get item category
                dict_of_everything[barcode[0].text[9:]] = [specific_name[0].text, item_category[0].text.split(">")[-1]]
            except:
                pass
        time.sleep(10)
        driver.get(current_url + "/" + str(page_num))

json_format = [{'barcode': k, "item name, item category": v} for k, v in dict_of_everything.items()]
with open('soda_cans.json', 'w') as fp:
    json.dump(json_format, fp, indent=4)


#print(dict_of_everything)


