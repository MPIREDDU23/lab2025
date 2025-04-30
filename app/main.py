from fastapi import FastAPI, Request
from routers import books, frontend
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



app = FastAPI()
app.include_router(books.router, tags=["books"])
app.include_router(frontend.router)




if __name__   == 'main':
    import uvicorn
    uvicorn.app
