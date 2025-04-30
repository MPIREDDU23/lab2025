from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory= "app/templates")

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    text = {
        "title": "Welcome to the library",
        "content": "Hello!"
    }

    return templates.TemplateResponse(
        request=request, name="home.html",
        context={"text": text}
    )
