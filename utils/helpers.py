from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import time
import re
from datetime import datetime
import pytz

def activate_driver():          
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver_path = GeckoDriverManager().install()
    web_driver = webdriver.Firefox(service=Service(driver_path),options=firefox_options)
    return web_driver

def parse_sensex_index_data(sensex_data) -> dict:
    try:
        # Initialize an empty dictionary to store the results
        result = {}

        # Check if sensex_data is None
        if sensex_data is None:
            raise ValueError("sensex_data is None")

        # Extract the current value
        current_value = sensex_data.find('div', {'class': 'newsensexvalue'}).text.strip()
        result['current_value'] = current_value

        # Extract the change point and change percentage
        change_data = sensex_data.find('div', {'class': re.compile('redtext|greentext')}).text.strip().split()
        result['change_point'] = change_data[0]
        result['change_percentage'] = change_data[1]

        # Extract the date, time, and status
        date_time_status = sensex_data.find('div', {'class': 'topdatearea'}).text.strip().split('|')
        result['date'] = date_time_status[0].strip()
        result['time'] = date_time_status[1].strip()
        result['status'] = date_time_status[2].strip()

        # Return the result dictionary
        return result

    except Exception as e:
        IST = pytz.timezone('Asia/Kolkata')
        current_ist_time = datetime.now(IST)
        return {
            "current_value" : str(e),
            "change_point" : str(e),
            "change_percentage" : str(e),
            "date" : str(current_ist_time.date()),
            "time" : str(current_ist_time.time()),
            "status" : "N/A"
        }

def parse_nifty_index_data(stock_string:str):
    try:
        parts = stock_string.split()
        value = (parts[0].replace(',', ''))
        change = (parts[1])
        percent_change = (parts[2].strip('()%'))
        date = parts[3]
        time = parts[4]
        return {'value': value, 'change': change, 'percent_change': percent_change, 'date': date, 'time': time}
    except:
        return {"Error" : "Unable to parse fetched data"}
  
def get_data_bse_index(driver : webdriver.Firefox):
    url:str = "https://www.bseindia.com/sensex/code/16/"
    try:
        if driver is not None:
            driver.get(url)
            time.sleep(2.5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            sensex_value = soup.find('div', {'class': 'sensextextold'})
            if sensex_value is not None:
                sensex_value.text.strip()
                parsed_data = parse_sensex_index_data(sensex_value)
                return parsed_data
    except Exception as e:
        return {e}
    finally:
        if driver is not None:
            driver.quit()  
                            
def get_data_nse_index(driver:webdriver.Firefox):
    try:
        url = "https://nseindia.com"
        if driver is not None:
            driver.get(url)
            time.sleep(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,"html.parser")
            # print(soup)
            nifty_div = soup.find('div', {'class': 'mkt_widget'})
            if nifty_div is not None:
                nifty_div = nifty_div.text.strip()
                return parse_nifty_index_data(nifty_div)
    finally:
        if driver is not None:
            driver.quit()
