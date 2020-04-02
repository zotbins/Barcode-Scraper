from selenium import webdriver
import time
import json

driver = webdriver.Chrome("Your/local/path/to/chromedriver") #for example /Users/josephtang/PycharmProjects/FirstSeleniumTest/drivers/chromedriver
driver.get("https://www.barcodelookup.com/")
time.sleep(15) #Use this time to manually fill out first captcha; only shows up on first entry
driver.find_element_by_name("search-input").send_keys("sode_cans" + Keys.ENTER)
current_url = driver.current_url
#time.sleep(10)

dict_of_everything = {} #key = barcode, values = list[item name, item category]

for page_num in range(2,1000): #each item has 1000 pages to go through
        ids = driver.find_elements_by_xpath("//*[@class = 'product-search-item']")
        item_names = [] # holds all the href values for each item
        for i in ids:
            item_names.append(i.get_attribute("href"))

        for i in item_names: #go through list of href values
            try:
                specific_name = driver.find_elements_by_xpath("//*[@href = '" + i + "']/li/div[2]/p[1]") #to get item names
                barcode = driver.find_elements_by_xpath("//*[@href = '" + i + "']/li/div[2]/p[2]") #to get barcode numbers
                item_category = driver.find_elements_by_xpath("//*[@href = '" + i + "']/li/div[2]/p[3]") # to get item category
                dict_of_everything[barcode[0].text[9:]] = [specific_name[0].text, item_category[0].text.split(">")[-1]]
            except:
                pass
        time.sleep(10) #waits 10 seconds between each search to avoid captcha problem
        driver.get(current_url + "/" + str(page_num))

json_format = [{'barcode': k, "item name, item category": v} for k, v in dict_of_everything.items()]
with open('soda_cans.json', 'w') as fp:
    json.dump(json_format, fp, indent=4)



