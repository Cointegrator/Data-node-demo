

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


    
    #URL of the page to be scraped
    url = 'https://coinranking.com/coins/gainers'
    

    
    options = Options()
    #options.add_argument('--headless') 
    
    driver = webdriver.Chrome(options=options) 
    driver.get(url)

    time.sleep(4)


    # Find the <tbody> element by CSS selector
    tbody_element = driver.find_element(By.CSS_SELECTOR, 'tbody.table__body')

    # Find all <a> elements with class "profile__link" within the <tbody> element
    a_elements = tbody_element.find_elements(By.CSS_SELECTOR, 'a.profile__link')
    c_elements = tbody_element.find_elements(By.CSS_SELECTOR, 'div.change.change--light')

    # Loop through the list of <a> elements and print their text
    # Loop through the list of <a> elements and print their text
    a_list=[]
    c_list=[]
    for a_element,c_element in zip(a_elements,c_elements):
        #print(a_element)
        print(a_element.text.strip())  # Use strip() to remove leading/trailing whitespace
        print(c_element.text.strip())
        a_list.append(a_element.text.strip())
        c_list.append(c_element.text.strip())

    # Create a DataFrame from the lists
    data = {'Coin name': a_list, 'Percentage change': c_list}
    df = pd.DataFrame(data)

    # Display the DataFrame
    print(df)
    # Save the DataFrame to a CSV file
    current_time = time.localtime()
    formatted_time = time.strftime("%H", current_time)

    print(formatted_time)
    df.to_csv(f'coinranking_top_gainers_{formatted_time}.csv', index=False)

    
    time.sleep(4)
    
    driver.quit()
    print("Finished scraping")




def main_run():
    """
    Main function to execute the cron job tasks.

    This function coordinates the entire process of fetching stock data,
    dividing the data into partitions, and inserting data into the database.
    """
    scrape_coinranking()


if __name__ == "__main__":
    main_run()

