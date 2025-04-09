from fastapi import FastAPI
from models import Book
from data.books import books

app = FastAPI()

@app.get("/books") 
def get_all_books() -> list[Book]:
    """ Get all books. """
    return list(books.values())
