# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:20:29 2022

@author: wmd852
"""
from scraper import dhl_scraper

def main():
    """
    Main methode to start the programm.

    Returns
    -------
    None.

    """
    print("Crawler starts.")
    scraper = dhl_scraper()
    scraper.run()
    print("Crawler finished.")
    
###Start programm###
if __name__ == "__main__":
    main()