# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:20:29 2022

@author: wmd852
"""
import sys
from scraper import dhl_scraper, ups_scraper, hermes_scraper, gls_scraper, dpd_scraper

def main(modus):
    """
    Main methode to start the programm.
    modus 1 = scrap data from https://www.dhl.de
    modus 2 = scrap data from https://www.ups.com.
    modus 3 = scrap data from https://www.myhermes.de/
    modus 4 = scrap data from https://www.gls-pakete.de
    modus 5 = scrap data from https://my.dpd.de/

    Returns
    -------
    None.

    """
    ###Crawl DHL###
    if modus == "1":
        print("go")
        scraper_dhl = dhl_scraper()
        scraper_dhl.run()
     ###Crawl UPS###
    if modus == "2":
         scraper_ups = ups_scraper()
         scraper_ups.run()
     ###Crawl Hermes###
    if modus == "3":
        scraper_hermes = hermes_scraper()
        scraper_hermes.run()
     ###Crawl GLS###
    if modus == "4":
        scraper_gls = gls_scraper()
        scraper_gls.run()
     ###Crawl DPD###
    if modus == "5":
        scraper_dpd = dpd_scraper()
        scraper_dpd.run()

    print("Crawler finished.")
    
###Start programm###
if __name__ == "__main__":
    main(sys.argv[1])