from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
import time


client = MongoClient('127.0.0.1', 27017)
db = client['db_mail_ru']
hits = db.hits

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)

driver.get('https://www.mvideo.ru/')

WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"h2")][contains(text(),"Хиты продаж")]')))

h2_list = driver.find_elements_by_xpath('//div[contains(@class,"h2")]')
hits_index = None
for i in range(len(h2_list)):
    if 'Хиты' in h2_list[i].text:
        hits_index = i
        break

carousel_list = driver.find_elements_by_xpath('//ul[contains(@data-init,"galleryCarousel")]')
new_list = []

while True:
    product_card_list = carousel_list[hits_index].find_elements_by_xpath('./li/div')

    for i in range(4):
        new_dict = {}

        new_dict['name'] = product_card_list[i].find_element_by_xpath('.//h4').get_attribute('title')
        new_dict['price'] = product_card_list[i].find_element_by_xpath(
            './/div[contains(@data-sel,"div-price_current")]').text.replace(' ', '')[:-1]
        pprint(new_dict)
        hits.insert_one(new_dict)
    next_page = carousel_list[hits_index].find_element_by_xpath('./../../a[contains(@class,"next-btn")]')

    if 'disabled' in next_page.get_attribute('class'):
        break

    next_page.click()
    time.sleep(5)
    
