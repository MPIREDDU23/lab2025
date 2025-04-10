from fastapi import APIRouter
from models.book import Book
from data.books import books

# / è il root path, ovvero la radice dell'applicazione
# ad esempio http://localhost:8000/ quindi il primo livello
# dell' host (in questo caso localhost) 

# books è al secondo livello
# se definiamo sotto livelli di /books
# /books/{id}
# /books/{id}/review
router = APIRouter(prefix="/books")

@router.get("/")
def get_all_books() -> list[Book]:
    """ Get all books. """
    return list(books.values())