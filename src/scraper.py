# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:20:41 2022

@author: Moritz Wegener - moritz.wegener@uni-koeln.de
@TODO - Catches und Logger
"""
import pandas as pd
import time
import pickle
import logging
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import os


class scraper:
    """
    Basic scraper class. Used by the specific scrapers.
    """
    def __init__(self):
        """
        Empty constructor.

        Returns
        -------
        None.

        """
        
        pass
    
    
    
    def get_zip_codes(self):
        """
        Get all zip codes where you want to get data for

        Returns
        -------
        None.

        """
        zip_code_list = pd.read_csv("../zip_codes_full.csv",encoding="utf-8",dtype ={"ZIP":str})
        return zip_code_list
    def run(self):
        """
        Run the crawler. First get all zip codes from the input file, then crawl data for all zip codes and store the data in the output folder.

        Returns
        -------
        None.

        """
        zip_code_list = self.get_zip_codes()
        self.get_data_list(zip_code_list)



class dhl_scraper(scraper):
    """
    Scraper class that extracts all DHL Shops for specific zip codes. Limit per zip code is 100.
    """
    def get_data_list(self,zip_code_list):
        """
        Crawl data for all zip codes. Currently acces ID, name, Adress, zip code and city of the shop. Loops through each zip code and extracts the data for every shop in this zip codes. Then concats the shops from all zip codes to get a merged result and avoid duplicates.

        Parameters
        ----------
        zip_code_list : dataframe
            List with all zip codes that the crawler should use.

        Returns
        -------
        None.

        """
        result_id = [] 
        result_dataset = []
        ###Set logger###
        logger = logging.Logger('DHL Logger')
        fh = logging.FileHandler("../log/dhl.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
        ###Start Data extraction###
        for zip_code in zip_code_list["ZIP"]:
            logger.warning("Get Data for zip code " + str(zip_code))
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe',options=options,service_log_path=os.path.devnull)
            try:
                
                
                url_for_zip_code = 'https://www.dhl.de/de/privatkunden/dhl-standorte-finden.html?address='+ str(zip_code)
                driver.get(url_for_zip_code)
                ###short delay so everthink gets loaded and the crawler is not to agressiv :)###
                time.sleep(4)
                ###get all listed shops###
                shop_list = driver.find_element_by_class_name("List__ResultListContent-sc-rockhr-5").find_elements_by_class_name("list-item-template")
                
                for shop in shop_list:
                    ###get values###
                    shop_id = shop.find_element_by_class_name("ListItemTemplate__ContentTitle-sc-j2blya-2").get_attribute('innerHTML')
                    try:
                        shop_name = shop.find_element_by_class_name("ListItemTemplate__ContentName-sc-j2blya-4").get_attribute('innerHTML').lower().replace("&amp;","&")
                    
                    except NoSuchElementException:
                        shop_name = "N/A" 
                    shop_adress_full = shop.find_element_by_class_name("ListItemTemplate__ContentAdress-sc-j2blya-5").get_attribute('innerHTML').lower()
                    street = shop_adress_full.split(" <br> ")[0].lower()
                    zip_code = shop_adress_full.split(" <br> ")[1].split(" ")[0].lower()
                    city = shop_adress_full.split(" <br> ")[1].split(" ")[1].lower()
                    if shop_id not in result_id:
                        result_id.append(shop_id)
                        result_dataset.append({'id':shop_id,'name':shop_name,'street':street,'zip_code':zip_code,'city':city})
                    else:
                        pass
            except Exception as e:
                logging.warning("Error getting data from" + str(zip_code))
                logging.error(traceback.format_exc())
                print("Error with zip code" + str(zip_code))
            ####close driver###
            driver.close()
            ###create output###    
            result_frame = pd.DataFrame(result_dataset)
            result_frame.to_csv(path_or_buf='../results/shop_list_dhl.csv',index=False,encoding='utf-8-sig')
       


           
class ups_scraper(scraper):
    """
    Scraper class that extracts all UPS Shops for specific zip codes. Limit per zip code is 100.
    """ 
    def get_data_list(self,zip_code_list):
        """
        Crawl data for all zip codes. Currently acces ID, name, Adress, zip code and city of the shop. For each zip code the limit of shops per page are 20. Per zip code the limit of pages is 5. So the total limit are 100 shops. Loops through each zip code, acces the shops per page and extracts the data for every shop on the page. Then concats the shops from all pages and zip codes to get a merged result and avoid duplicates.

        Parameters
        ----------
        zip_code_list : dataframe
            List with all zip codes that the crawler should use.

        Returns
        -------
        None.

        """
        result_id = [] 
        result_dataset = []
        ###Set logger###
        logger = logging.Logger('UPS Logger')
        fh = logging.FileHandler("../log/ups.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
        ###Start getting data###
        for zip_code in zip_code_list["ZIP"]:
            ###Write Log for new crawler###
            logger.warning("Get Data for zip code " + str(zip_code))
            ###print progrss to console##
            print("Get Data for zip code " + str(zip_code))
            ###set webdriver options###
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe',options=options,service_log_path=os.path.devnull)
            try:
                ###load cookies of website###
                cookies = pickle.load(open("../webdriver/cookies_ups.pkl", "rb"))
                driver.get("https://www.ups.com/dropoff?loc=de_DE")
                for cookie in cookies:
                    driver.add_cookie(cookie)
                ###Acces website and search###
                driver.get("https://www.ups.com/dropoff?loc=de_DE")
                time.sleep(5)
                driver.find_element_by_id("txtQuery").send_keys(zip_code)
                driver.find_element_by_class_name("searchBtn").click()
                time.sleep(5)
                ###Start getting the data###
                shop_list = []
                ###Loop pages max number of pages is 5###
                for i in range(0,6):
                    ###extract stores from first page##
                    if i == 0:
                        try:
                            shop_list = driver.find_element_by_class_name("mappedResultList").find_elements_by_tag_name("li")
                            
                        except NoSuchElementException:
                            break
                    ###extract stores from page number bigger than one###
                    else:
                        try:
                            driver.find_element_by_id("nextLinkId").click()
                            shop_list = driver.find_element_by_class_name("mappedResultList").find_elements_by_tag_name("li")
                        except NoSuchElementException:
                            break
                    ###extract values###
                    for shop in shop_list:
                        shop_id = shop.get_attribute('id')
                    
                        shop_name = shop.find_element_by_class_name("seccol5").find_elements_by_tag_name('span')[2].get_attribute('innerHTML').replace("&amp;","&").lower()
                        street = shop.find_element_by_class_name("seccol5").find_elements_by_tag_name('span')[3].get_attribute('innerHTML').split(", ")[0].lower()
                        zip_code = shop.find_element_by_class_name("seccol5").find_elements_by_tag_name('span')[3].get_attribute('innerHTML').split(", ")[1]
                        city = shop.find_element_by_class_name("seccol5").find_elements_by_tag_name('span')[3].get_attribute('innerHTML').split(", ")[2].replace("<br>","").lower().strip()
                        ###merge data##
                        if shop_id not in result_id:
                            result_id.append(shop_id)
                            result_dataset.append({'id':shop_id,'name':shop_name,'street':street,'zip_code':zip_code,'city':city})
                        else:
                            pass
            except Exception as e:
                logger.warning("Error getting data from" + str(zip_code))
                logger.error(traceback.format_exc())
                print("Error with zip code" + str(zip_code))
            ###close driver###            
            driver.close()
            ###create output###
            result_frame = pd.DataFrame(result_dataset)
            result_frame.to_csv(path_or_buf='../results/shop_list_ups.csv',index=False,encoding='utf-8-sig')
        



class hermes_scraper(scraper):
    """
    Scraper class that extracts all UPS Shops for specific zip codes. Limit per zip code is 20.
    """
    def get_data_list(self,zip_code_list):
        result_id = [] 
        result_dataset = []
        ###Set logger###
        logger = logging.Logger('hermes Logger')
        fh = logging.FileHandler("../log/hermes.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
        ###Start getting data###
        for zip_code in zip_code_list["ZIP"]:
            logger.warning("Get Data for zip code " + str(zip_code))
            ###print progrss to console##
            print("Get Data for zip code " + str(zip_code))
            ###set webdriver options###
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe',options=options,service_log_path=os.path.devnull)
            try:
                driver.get("https://www.myhermes.de/paketshop/")
                time.sleep(2)
                try:
                    driver.find_element_by_class_name("uc-btn-accept").click()
                except Exception as e:
                    pass
                time.sleep(1)
                driver.refresh()
                time.sleep(2)
                driver.switch_to.frame(driver.find_element_by_id("iframe67345"))
                driver.find_element_by_xpath("//input[@placeholder='Adresse, PLZ oder Ort eingeben']").send_keys(str(zip_code))
                driver.find_element_by_class_name("btn-primary").click()
                time.sleep(2)
                shop_list = driver.find_elements_by_class_name("shop-list-item")
                for shop in shop_list:
                    shop_name = shop.find_element_by_class_name("t-h3").get_attribute('innerHTML').lower()
                    street = shop.find_element_by_class_name("address").get_attribute('innerHTML').split(",  ")[0]
                    zip_code = shop.find_element_by_class_name("address").get_attribute('innerHTML').split(",  ")[1].split(" ")[0]
                    city = shop.find_element_by_class_name("address").get_attribute('innerHTML').split(",  ")[1].split(" ")[1]
                    shop_id = shop_name+street+city+str(zip_code)
                ###merge data##
                    if shop_id not in result_id:
                        result_id.append(shop_id)
                        result_dataset.append({'id':shop_id,'name':shop_name,'street':street,'zip_code':zip_code,'city':city})
                    else:
                        pass
            except Exception as e:
                logger.warning("Error getting data from" + str(zip_code))
                logger.error(traceback.format_exc())
                print("Error with zip code" + str(zip_code))
            ###close driver###            
            driver.close() 
            ###create output###
            result_frame = pd.DataFrame(result_dataset)
            result_frame.to_csv(path_or_buf='../results/shop_list_hermes.csv',index=False,encoding='utf-8-sig')
        
     
        
            
class gls_scraper(scraper):
    """
    Scraper class that extracts all GLS Shops for specific zip codes. Limit per zip code is 25.
    """ 
    def get_data_list(self,zip_code_list):
        """
        Crawl data for all zip codes. Currently acces ID, name, Adress, zip code and city of the shop. Loops through each zip code and extracts the data for every shop in this zip codes. Then concats the shops from all zip codes to get a merged result and avoid duplicates.

        Parameters
        ----------
        zip_code_list : dataframe
            List with all zip codes that the crawler should use.

        Returns
        -------
        None.

        """
        result_id = [] 
        result_dataset = []
        ###Set logger###
        logger = logging.Logger('GLS Logger')
        fh = logging.FileHandler("../log/gls.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
        for zip_code in zip_code_list["ZIP"]:
            ###print progress to log###
            logger.warning("Get Data for zip code " + str(zip_code))
            ###print progrss to console##
            print("Get Data for zip code " + str(zip_code))
            ###set webdriver options###
            options = Options()
            options.add_argument("--headless")
            ###Acces website and search###
            try:
                driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe',options=options,service_log_path=os.path.devnull)
                
                driver.get("https://www.gls-pakete.de/paketshop-finden?location="+str(zip_code))
                time.sleep(4)
                shop_list = driver.find_elements_by_class_name("contact-card")
                for shop in shop_list:
                    shop_name = shop.find_element_by_class_name("shop__heading").find_element_by_class_name("h5").get_attribute('innerHTML').lower()
                    street = shop.find_elements_by_class_name("mb-2")[0].get_attribute('innerHTML').split("<br>")[0].lower()
                    zip_code = shop.find_elements_by_class_name("mb-2")[0].get_attribute('innerHTML').split("<br>")[1].split(" ")[0]
                    city = shop.find_elements_by_class_name("mb-2")[0].get_attribute('innerHTML').split("<br>")[1].split(" ")[1]
                    shop_id = shop.find_elements_by_class_name("mb-2")[1].get_attribute('innerHTML')
                ###merge data##
                    if shop_id not in result_id:
                        result_id.append(shop_id)
                        result_dataset.append({'id':shop_id,'name':shop_name,'street':street,'zip_code':zip_code,'city':city})
                    else:
                        pass
            except Exception as e:
                logger.warning("Error getting data from" + str(zip_code))
                logger.error(traceback.format_exc())
                print("Error with zip code" + str(zip_code))
            ###close driver###            
            driver.close()
            ###create output###
            result_frame = pd.DataFrame(result_dataset)
            result_frame.to_csv(path_or_buf='../results/shop_list_gls.csv',index=False,encoding='utf-8-sig')
        
        
        

class dpd_scraper(scraper):
    """
    Scraper class that extracts all DPD Shops for specific zip codes. Limit per zip code is 25.
    """ 
    
    def get_data_list(self,zip_code_list):
        """
        Crawl data for all zip codes. Currently acces ID, name, Adress, zip code and city of the shop. Loops through each zip code and extracts the data for every shop in this zip codes. Then concats the shops from all zip codes to get a merged result and avoid duplicates.

        Parameters
        ----------
        zip_code_list : dataframe
            List with all zip codes that the crawler should use.

        Returns
        -------
        None.
        @TODO - Anpassen
        """
        result_id = [] 
        result_dataset = []
        ###Set logger###
        logger = logging.Logger('DPD Logger')
        fh = logging.FileHandler("../log/dpd.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(fh)
        for zip_code in zip_code_list["ZIP"]:
            ###print progress to log###
            logger.warning("Get Data for zip code " + str(zip_code))
            ###print progrss to console##
            print("Get Data for zip code " + str(zip_code))
            ###set webdriver options###
            options = Options()
            options.add_argument("--headless")
            ###Acces website and search###
            try:
                driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe',options=options,service_log_path=os.path.devnull)
                ###load cookies###
                cookies = pickle.load(open("../webdriver/cookies_dpd.pkl", "rb"))
                driver.get("https://my.dpd.de/shopfinder.aspx?src="+str(zip_code))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.get("https://my.dpd.de/shopfinder.aspx?src="+str(zip_code))
                time.sleep(3)
                ###load all results###
                end_of_results = False
                while end_of_results == False:
                    try: 
                        driver.find_element_by_id("ContentPlaceHolder1_modShopFinder_repShopList_btnFindMoreShops").click()
                        time.sleep(2)
                    except Exception as e:
                        end_of_results = True
                ###extract data###
                shop_list = driver.find_elements_by_class_name("Shop")
                for shop in shop_list:
                    shop_name = shop.find_elements_by_class_name("labSub13")[0].get_attribute('innerHTML').lower()
                    street = shop.find_elements_by_class_name("labSub13")[1].get_attribute('innerHTML').lower().replace("&nbsp;"," ")
                    zip_code = shop.find_elements_by_class_name("labSub13")[2].get_attribute('innerHTML').lower().split("&nbsp;")[0]
                    city = shop.find_elements_by_class_name("labSub13")[2].get_attribute('innerHTML').lower().split("&nbsp;")[1]
                    shop_id = shop_name+street+city+str(zip_code)
                    if shop_id not in result_id:
                        result_id.append(shop_id)
                        result_dataset.append({'id':shop_id,'name':shop_name,'street':street,'zip_code':zip_code,'city':city})
                    else:
                        pass
            except Exception as e:
                logger.warning("Error getting data from" + str(zip_code))
                logger.error(traceback.format_exc())
                print("Error with zip code" + str(zip_code))
            ####close driver###
            driver.close()  
            ###create output###    
            result_frame = pd.DataFrame(result_dataset)
            result_frame.to_csv(path_or_buf='../results/shop_list_dpd.csv',index=False,encoding='utf-8-sig')