from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from routers.users import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse, status_code=200)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, status_code=200)
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/home", response_class=HTMLResponse)
def get_home(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "user": user})

@router.get("/dev", response_class=HTMLResponse, status_code=200)
def get_admin(request: Request):
    return templates.TemplateResponse("dev.html", {"request": request})


@router.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon/favicon.ico")
