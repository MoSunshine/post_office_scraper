# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:20:41 2022

@author: wmd852
"""
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class dhl_scraper:
    """
    Scraper class that extracts all DHL Shops for specific zip codes
    """
    
    
    def __init__(self):
        """
        Empty constructor.

        Returns
        -------
        None.

        """
        pass
    
    
    
    def run(self):
        """
        Run the crawler. First get all zip codes from the input file, then crawl data for all zip codes and store the data in the output folder.

        Returns
        -------
        None.

        """
        zip_code_list = self.get_zip_codes()
        self.get_data_list(zip_code_list)
    
    
    
    def get_zip_codes(self):
        """
        Get all zip codes where you want to get data for

        Returns
        -------
        None.

        """
        zip_code_list = pd.read_csv("../zip_codes.csv",encoding="utf-8")
        return zip_code_list
    
    
    
    def get_data_list(self,zip_code_list):
        """
        Crawl data for all zip codes. Currently acces ID, name, Adress, zip code and city of the shop.

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
        for zip_code in zip_code_list["ZIP"]:
            driver = webdriver.Firefox(executable_path='..\webdriver\geckodriver.exe')
            url_for_zip_code = 'https://www.dhl.de/de/privatkunden/dhl-standorte-finden.html?address='+ str(zip_code)
            driver.get(url_for_zip_code)
            ##short delay so everthink gets loaded and the crawler is not to agressiv :) 
            time.sleep(10)
            ##get all listed shops
            shop_list = driver.find_element_by_class_name("List__ResultListContent-sc-rockhr-5").find_elements_by_class_name("list-item-template")
            
            for shop in shop_list:
                ##get values
                shop_id = shop.find_element_by_class_name("ListItemTemplate__ContentTitle-sc-j2blya-2").get_attribute('innerHTML')
                try:
                    shop_name = shop.find_element_by_class_name("ListItemTemplate__ContentName-sc-j2blya-4").get_attribute('innerHTML')
                
                except NoSuchElementException:
                    shop_name = "N/A" 
                shop_adress_full = shop.find_element_by_class_name("ListItemTemplate__ContentAdress-sc-j2blya-5").get_attribute('innerHTML')
                street = shop_adress_full.split(" <br> ")[0]
                zip_code = shop_adress_full.split(" <br> ")[1].split(" ")[0]
                city = shop_adress_full.split(" <br> ")[1].split(" ")[1]
                if shop_id not in result_id:
                    result_id.append(shop_id)
                    result_dataset.append({'id':shop_id,'name':shop_name,'street':street,'zip_code':zip_code,'city':city})
                else:
                    pass
            #close driver 
            driver.close()
             
        result_frame = pd.DataFrame(result_dataset)
        result_frame.to_csv(path_or_buf='../results/shop_list.csv',index=False,encoding='utf-8-sig')
           
        
        
        