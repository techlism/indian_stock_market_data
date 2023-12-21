from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
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
    driver = None
    try:
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver_path = GeckoDriverManager().install()
        driver = webdriver.Firefox(service=Service(driver_path),options=firefox_options)
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        sensex_value = soup.find('div', {'class': 'sensextextold'}).text.strip()
        parsed_data = parse_stock_data(sensex_value)
        return parsed_data
    finally:
        if driver is not None:
            driver.quit()

app = FastAPI()

@app.get("/")
async def base():
    try:
        response={"Base-Address":"No content is present in this address"}
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))

@app.get("/sensex-value")
async def get_sensex():
    try:
        sensex_url = "https://www.bseindia.com/sensex/code/16/"
        sensex_data = get_data_bse(sensex_url)
        return JSONResponse(content=sensex_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        
