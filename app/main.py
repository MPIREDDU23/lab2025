#!/opt/homebrew/bin/python3

from fastapi import FastAPI, Request
from routers import books, frontend
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(books.router, tags=["books"])
app.include_router(frontend.router)
app.mount("/static", StaticFiles(directory="app/static") , name="static")



if __name__   == 'main':
    import uvicorn
    uvicorn.app
