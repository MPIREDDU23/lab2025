#!/Users/marcopireddu/miniconda3/envs/pw/bin/python

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.db import SessionDep
from sqlmodel import select
from models.book import Book

templates = Jinja2Templates(directory= "app/templates")

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    text = {
        "title": "Welcome to the library",
        "content": "Hello!"
    }

    return templates.TemplateResponse(
        request=request, name="home.html",
        context={
            "text": text
                 }
    )

@router.get("/book_list", response_class=HTMLResponse)
def show_book_list(request: Request, session: SessionDep):
    statement = select(Book)
    books = session.exec(statement).all()
    context = {"books" : books}

    title = 2
    return templates.TemplateResponse(
        request=request,
        name="list.html",
        context=context
    )

@router.get("/add_book_form", response_class=HTMLResponse)
async def add_book_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add.html"
    )