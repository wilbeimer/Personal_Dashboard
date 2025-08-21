from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import frontend, users

app = FastAPI()

app.include_router(users.router)
app.include_router(frontend.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
