# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:20:29 2022

@author: wmd852
"""
from scraper import dhl_scraper, ups_scraper, hermes_scraper, gls_scraper, dpd_scraper

def main():
    """
    Main methode to start the programm.

    Returns
    -------
    None.

    """
    print("Crawler starts.")
    ###Crawl DHL###
    #scraper_dhl = dhl_scraper()
    #scraper_dhl.run()
    ###Crawl UPS###
    #scraper_ups = ups_scraper()
    #scraper_ups.run()
    ###Crawl Hermes der knallt noch###
    #scraper_hermes = hermes_scraper()
    #scraper_hermes.run()
    ###Crawl GLS###
    #scraper_gls = gls_scraper()
    #scraper_gls.run()
    ###Crawl DPD###
    print("Crawler finished.")
    
###Start programm###
if __name__ == "__main__":
    main()