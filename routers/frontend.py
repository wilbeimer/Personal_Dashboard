from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse, status_code=200)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/home", response_class=HTMLResponse, status_code=200)
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
