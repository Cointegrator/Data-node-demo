

import time

from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re
import datetime
from datetime import datetime
from datetime import datetime, timedelta
#from statsmodels.nonparametric.smoothers_lowess import lowess
#import matplotlib.dates as mdates
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import re

import sys
import subprocess




#import matplotlib.pyplot as plt
import pandas as pd



def scrape_coinranking():


    options = Options()
    #options.add_argument('--headless') 
    
    driver = webdriver.Chrome(options=options) 
    


    # Read the CSV file into a DataFrame
    url_list = pd.read_csv("description_11PM.csv")

    print(url_list.head())

    description_list=[]
    
    for index, row in url_list.iterrows():
        coin_name = row['Coin name']
        url = row['link']
        driver.get(url)

        # Find the <p> element within the article element
        p_element = driver.find_element(By.CSS_SELECTOR, 'p')

        # Now you have a reference to the <p> element
        # You can access its text content using the `text` attribute
        p_text = p_element.text[14:-5]
        description_list.append(p_text)
        # Do something with the values (e.g., print them)
        #print(f'Coin Name: {coin_name}')
        #print(f'Link: {url}')
        #print('-' * 20)  # Just to separate the output for each row

    url_list['description_list']=description_list
    print(url_list.head())
    url_list.to_csv('collected_description_11PM.csv')

def main_run():
    """
    Main function to execute the cron job tasks.

    This function coordinates the entire process of fetching stock data,
    dividing the data into partitions, and inserting data into the database.
    """
    scrape_coinranking()


if __name__ == "__main__":
    main_run()

