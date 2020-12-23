from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from backend.utils import is_path, is_file_link, is_list
from backend import eiger, git
import jinja2
import backend.config as cfg

app = FastAPI()
app.mount("/gitrepo", StaticFiles(directory=cfg.git_path), name="gitrepo")
app.mount("/media", StaticFiles(directory="media/"), name="media")


templates = Jinja2Templates(directory="templates/")
templates.env.tests["Path"] = is_path
templates.env.tests["FileLink"] = is_file_link
templates.env.tests["list"] = is_list
templates.env.globals.update(last_commit=git.last_commit, branch=git.branch)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/eiger")
def read_eiger():
    return {"Hello": "Eiger"}


@app.get("/eiger/feb")
def read_febs(request: Request):
    result = eiger.get_febs()
    return templates.TemplateResponse(
        "feb.html", context={"request": request, "result": result}
    )


@app.get("/eiger/beb")
def read_bebs(request: Request):
    result = eiger.get_bebs()
    return templates.TemplateResponse(
        "beb.html", context={"request": request, "result": result, 'mounted': eiger.get_mounted_bebs()}
    )


@app.get("/eiger/feb/{full_id}")
def read_feb_info(request: Request, full_id: str):
    result = eiger.get_feb_info(full_id)
    return templates.TemplateResponse(
        "board_info.html",
        context={"request": request, "result": result, "title": "Front"},
    )


@app.get("/eiger/beb/{full_id}")
def read_feb_info(request: Request, full_id: str):
    result = eiger.get_beb_info(full_id)
    return templates.TemplateResponse(
        "board_info.html",
        context={"request": request, "result": result, "title": "Back"},
    )


@app.get("/eiger/module")
def read_modules(request: Request):
    result = eiger.get_modules()
    return templates.TemplateResponse(
        "module.html",
        context={
            "request": request,
            "result": result,
            "mounted": eiger.get_mounted_modules(),
        },
    )


@app.get("/eiger/module/{full_id}")
def read_feb_info(request: Request, full_id: str):
    result = eiger.EigerModule().load(full_id)
    return templates.TemplateResponse(
        "module_info.html",
        context={
            "request": request,
            "result": result,
        },
    )


@app.get("/eiger/system")
def read_modules(request: Request):
    result = eiger.get_systems()
    return templates.TemplateResponse(
        "system.html", context={"request": request, "result": result}
    )


@app.get("/eiger/system/{full_id}")
def read_system_info(request: Request, full_id: str):
    result = eiger.get_system_info(full_id)
    return templates.TemplateResponse(
        "system_info.html",
        context={"request": request, "result": result, "title": full_id},
    )


@app.get('/about')
def about(request: Request):
    result = eiger.get_timings()
    return templates.TemplateResponse(
        "about.html",
        context={"request": request, "result": result,},
    )
