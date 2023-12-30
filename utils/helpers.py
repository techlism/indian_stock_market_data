from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import re

def activate_driver():          
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver_path = GeckoDriverManager().install()
    web_driver = webdriver.Firefox(service=Service(driver_path),options=firefox_options)
    return web_driver

def parse_sensex_index_data(data):
  # Split the data into individual components
  components = data.split()

  # Extract and format values
  current_value = (components[0].replace(",", ""))
  change_point = (components[1].replace(",", ""))
  change_percentage = (components[2].replace("%", ""))
  date = components[3]+" "+components[4]+" "+components[5]
  time = components[7]
  status = components[9]

  # Return data as a dictionary
  return {
      "current_value": current_value,
      "change_point": change_point,
      "change_percentage": change_percentage,
      "date": date,
      "time": time,
      "status": status,
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
  
def get_data_bse_index(url:str,driver : webdriver.Firefox):
    try:
        if driver is not None:
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            sensex_value = soup.find('div', {'class': 'sensextextold'}).text.strip()
            parsed_data = parse_sensex_index_data(sensex_value)
            return parsed_data
    finally:
        if driver is not None:
            driver.quit()  

def create_url_from_data(response: dict):
    # in bseindia security_name and security_id are reduntant(we can put anything as placeholder) it primarily uses security_code
    base = "https://www.bseindia.com/stock-share-price/"
    for code, data in response.items():
        security_name = data['Security-Name'].lower().replace(' ', '-').replace('&', '').replace('.', '')
        security_id = data['Security-Id'].lower()
        url = f"{base}{security_name}/{security_id}/{code}/"
        return url

    
                
def get_stock_data(response:dict,driver : webdriver.Firefox) -> BeautifulSoup:
    try :
        url = create_url_from_data(response)
        if driver is not None:
            driver.get(url)
            # Wait until an element with the tag name 'body' is loaded.
            WebDriverWait(driver, 5.0).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,"html.parser")
            return soup
    finally:
        if driver is not None:
            driver.quit()    

            
def get_data_nse_index(driver:webdriver.Firefox):
    try:
        url = "https://nseindia.com"
        if driver is not None:
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,"html.parser")
            # print(soup)
            nifty_div = soup.find('div', {'class': 'mkt_widget'}).text.strip()
            return parse_nifty_index_data(nifty_div)
    finally:
        if driver is not None:
            driver.quit()
