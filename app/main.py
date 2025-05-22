#!/Users/marcopireddu/miniconda3/envs/pw/bin/python

from fastapi import FastAPI
from routers import books, frontend, users
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from data.db import init_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    # yield # after this the function is in the context manager
    # on shutdown
    init_database()
    yield
    # on shutdown



app = FastAPI(lifespan=lifespan)
app.include_router(books.router, tags=["books"])
app.include_router(frontend.router)
app.include_router(users.router, tags=["users"])
app.mount("/static", StaticFiles(directory="app/static") , name="static")

if __name__   == 'main':
    import uvicorn
    uvicorn.app
