from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.eiger import get_febs, get_feb_info
app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})

@app.get("/eiger")
def read_eiger():
    return {"Hello": "Eiger"}

@app.get("/eiger/feb")
def read_febs(request: Request):
    result = get_febs()
    return templates.TemplateResponse('feb.html', context={'request':request, 'result': result})
    

@app.get("/eiger/feb/{full_id}")
def read_feb_info(request: Request, full_id: str):
    result = get_feb_info(full_id)
    return templates.TemplateResponse('feb_info.html', context={'request':request, 'result': result})
    

