from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

def parse_stock_data(data):
  # Split the data into individual components
  components = data.split()

  # Extract and format values
  current_value = float(components[0].replace(",", ""))
  change_point = float(components[1].replace(",", ""))
  change_percentage = float(components[2].replace("%", ""))
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


def get_data_bse(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        page_source = driver.page_source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        sensex_value = soup.find('div', {'class': 'sensextextold'}).text.strip()
        # print(sensex_value)
        parsed_data = parse_stock_data(sensex_value)
        # print(parsed_data)
        return parsed_data
    finally:
        driver.quit()

app = FastAPI()

@app.get("/")
async def base():
    try:
        response={"Base-Address":"No content is present in this address"}
        return JSONResponse(content=response)
    except Exception as e:
        return HTTPException(status_code=404,detail=str(e))

@app.get("/sensex-value")
async def get_sensex():
    try:
        sensex_url = "https://www.bseindia.com/sensex/code/16/"
        sensex_data = get_data_bse(sensex_url)
        return JSONResponse(content=sensex_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        
    
