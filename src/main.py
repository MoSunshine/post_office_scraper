# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:20:29 2022

@author: wmd852
"""
import sys
import logging
from scraper import dhl_scraper, ups_scraper, hermes_scraper, gls_scraper, dpd_scraper

def main(modus, rerun):
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
        scraper_dhl.run(rerun)
     ###Crawl UPS###
    if modus == "2":
         scraper_ups = ups_scraper()
         scraper_ups.run(rerun)
     ###Crawl Hermes###
    if modus == "3":
        scraper_hermes = hermes_scraper()
        scraper_hermes.run(rerun)
     ###Crawl GLS###
    if modus == "4":
        scraper_gls = gls_scraper()
        scraper_gls.run(rerun)
     ###Crawl DPD###
    if modus == "5":
        scraper_dpd = dpd_scraper()
        scraper_dpd.run(rerun)

    print("Crawler finished.")
    
###Start programm###
if __name__ == "__main__":
    logger = logging.Logger('main logger')
    fh = logging.FileHandler("../log/main.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)
    try:
        main(sys.argv[1],sys.argv[2])
    except Exception as e:
        logger.error(e)