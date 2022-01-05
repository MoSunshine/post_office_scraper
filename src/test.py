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
cookies = pickle.load(open("../webdriver/cookies_hermes.pkl", "rb"))
driver.get("https://www.myhermes.de/paketshop/")
time.sleep(2)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get("https://www.myhermes.de/paketshop/")    
time.sleep(15)
###write cookies###
driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe')
driver.get("https://www.myhermes.de/paketshop/")
time.sleep(20)
pickle.dump( driver.get_cookies() , open("../webdriver/cookies_hermes.pkl","wb"))