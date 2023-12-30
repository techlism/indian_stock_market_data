from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager
import csv
from utils.helpers import get_data_bse_index #sensex
from utils.helpers import get_data_nse_index #nifty
from utils.helpers import activate_driver
from fastapi.responses import HTMLResponse
#---------------------------------------------------

# data_dict = {}
web_driver = None

#----------------------------------------------------

@asynccontextmanager
async def load_csv_and_activate_driver(app:FastAPI):    
    # def load_csv():
    #     global data_dict
    #     with open('Equity.csv', mode ='r') as file:    
    #         csvFile = csv.DictReader(file)
    #         for row in csvFile:
    #             key = row.pop('Security-Code')
    #             data_dict[key] = row
    #     file.close()
    

                
    # load_csv()
    # activate_driver()
    yield

#----------------------------------------------------

app = FastAPI()

#----------------------------------------------------

@app.get("/")
async def base():
    try:
        response = {"Base-Address":"Nothing Here"}
        return JSONResponse(response)
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))

#----------------------------------------------------


#----------------------------------------------------

@app.get("/sensex-value")
async def get_sensex():
    try:
        web_driver = activate_driver()
        sensex_url = "https://www.bseindia.com/sensex/code/16/"
        sensex_data = get_data_bse_index(sensex_url,web_driver)
        return JSONResponse(content=sensex_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#----------------------------------------------------

#----------------------------------------------------

# @app.get("/get-data-from-code/{code}")
# async def base(code: str):
#     try:
#         data = {code : data_dict[code]}
#         response = get_stock_data(data,web_driver)
#         html_content = str(response)
#         return HTMLResponse(content=html_content)        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/nifty-value")
async def get_nifty():
    try:
        web_driver = activate_driver()        
        output = {"Sensex Value" : get_data_nse_index(web_driver)}
        return JSONResponse(content=output)
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e))

    
    