from fastapi import FastAPI, Request
from routers import books
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



app = FastAPI()
app.include_router(books.router, tags=["books"])
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="home.html",

    )


if __name__   == 'main':
    import uvicorn
    uvicorn.app
