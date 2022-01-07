# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 10:32:24 2022

@author: wmd852
"""
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pickle


###read cookies###
driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe')
cookies = pickle.load(open("../webdriver/cookies_dpd.pkl", "rb"))
driver.get("https://my.dpd.de/shopfinder.aspx?src=50969")
time.sleep(2)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get("https://my.dpd.de/shopfinder.aspx?src=50969")    
time.sleep(15)
###write cookies###
driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe')
driver.get("https://my.dpd.de/shopfinder.aspx?src=50969")
time.sleep(20)
pickle.dump( driver.get_cookies() , open("../webdriver/cookies_dpd.pkl","wb"))



###test hermes###
driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe')

driver.get("https://www.myhermes.de/paketshop/")
time.sleep(2)
driver.find_element_by_class_name("uc-btn-accept").click()
time.sleep(2)
driver.refresh()
time.sleep(2)
driver.switch_to.frame(driver.find_element_by_id("iframe67345"))
driver.find_element_by_xpath("//input[@placeholder='Adresse, PLZ oder Ort eingeben']").send_keys("50969")
driver.find_element_by_class_name("btn-primary").click()
shop_list = driver.find_elements_by_class_name("shop-list-item")




js_code = "return document.getElementsByTagName('html').innerHTML"
your_elements = driver.execute_script(js_code)


pickle.dump( your_elements , open("../webdriver/code.html","wb"))
# =============================================================================
# driver.find_element_by_id("uc-btn-accept-banner").click()
# time.sleep(2)
# driver.get("https://www.myhermes.de/paketshop/")
# time.sleep(5)
# driver.find_element_by_class_name("uc-btn-accept").click()
# time.sleep(2)
# html = driver.page_source
# pickle.dump( html , open("../webdriver/code.html","wb"))
# driver.find_element_by_class_name("search-input").find_element_by_class_name("form-control").send_keys("50969")
# driver.find_element_by_class_name("btn-primary").click()
# 
# =============================================================================
# =============================================================================
# 
# time.sleep(3)
# html = driver.page_source
# pickle.dump( html , open("../webdriver/code.html","wb"))
# print(html)
# driver.find_element_by_class_name("search-input").find_element_by_class_name("form-control").send_keys("50969")
# driver.find_element_by_class_name("btn-primary").click()
# time.sleep(3)
# shop_list = driver.find_elements_by_class_name("shop-list-item")
# =============================================================================
