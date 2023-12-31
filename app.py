# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from webdriver_manager.firefox import GeckoDriverManager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
# from contextlib import asynccontextmanager
# import csv
from utils.helpers import get_data_bse_index #sensex
from utils.helpers import get_data_nse_index #nifty
from utils.helpers import activate_driver
# from fastapi.responses import HTMLResponse
#---------------------------------------------------

app = FastAPI()

#----------------------------------------------------

@app.get("/")
async def base():
    try:
        response = {"Base-Address":"Nothing Here"}
        return JSONResponse(response)
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e)) from e

#----------------------------------------------------


#----------------------------------------------------

@app.get("/sensex-value")
async def get_sensex():
    """Route Function for /sensex-value"""
    try:
        web_driver = activate_driver()
        sensex_url = "https://www.bseindia.com/sensex/code/16/"
        sensex_data = get_data_bse_index(sensex_url,web_driver)
        return JSONResponse(content=sensex_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e   
#----------------------------------------------------

@app.get("/nifty-value")
async def get_nifty():
    """Route Function for /nifty-value"""
    try:
        web_driver = activate_driver()        
        output = {"Sensex Value" : get_data_nse_index(web_driver)}
        return JSONResponse(content=output)
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e)) from e