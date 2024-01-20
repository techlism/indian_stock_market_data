from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

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
        WEB_DRIVER = activate_driver()
        sensex_data = get_data_bse_index(WEB_DRIVER)
        output = {"Sensex Value" : sensex_data}
        return JSONResponse(content=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e   
#----------------------------------------------------


@app.get("/nifty-value")
async def get_nifty():
    """Route Function for /nifty-value"""
    try:
        WEB_DRIVER = activate_driver()        
        output = {"Nifty Value" : get_data_nse_index(WEB_DRIVER)}
        return JSONResponse(content=output)
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e)) from e