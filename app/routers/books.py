#!/opt/homebrew/bin/python3

from fastapi import APIRouter, Request, HTTPException, Path, Form #HTTPException serve per gestire le eccezioni
from models.book import Book
from models.review import Review
from data.books import books
from typing import Annotated # Annotated serve per annotare i parametri, definire il tipo di dato e
from pydantic import ValidationError
from fastapi.responses import RedirectResponse

# / è il root path, ovvero la radice dell'applicazione
# ad esempio http://localhost:8000/ quindi il primo livello
# dell' host (in questo caso localhost)

# books è al secondo livello
# se definiamo sotto livelli di /books
# /books/{id}
# /books/{id}/review

# /books/
router = APIRouter(prefix="/books")
@router.get("/")
def get_all_books(
    sort: bool = False
) -> list[Book]:
    """ Get all books. """
    if sort:
        return sorted(books.values(), key=lambda book: book.id)
    return list(books.values())

@router.post("/")
def add_book(
    book: Book
):
    """ Add a new book. """
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book ID already exists.")
        # 403 è il codice di errore per forbidden, quindi tipo accesso negato alla risorsa
        # è adatto al nostro caso, in cui il libro esiste già
    books[book.id] = book
    return "Book successfully added."

@router.post("_form/")
def add_book_from_form(
    request: Request,
    book: Annotated[Book, Form()]
):
    """ Add book from form. """
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book ID already exists.")
    books[book.id] = book
    url = request.url_for("show_book_list")
    return RedirectResponse(url=url, status_code=303)

@router.delete("/")
def delete_all_books():
    """ Delete all books. """
    books.clear()
    return "All books successfully deleted."

@router.delete("/{id}")
def delete_book(
    id: Annotated[int, Path(description="The ID of the book to delete.")]
):
    """ Delete the book with the given ID. """
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found.")
    del books[id]
    return "Book successfully deleted."


@router.put("/{id}")
def update_book(
    id: Annotated[int, Path(description="The ID of the book to update.")],
    book: Book
):
    """ Updates the book with the given ID. """
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found.")
    books[id] = book
    return "Book successfully updated."

# /books/{id}
@router.get("/{id}")
def get_book_by_id(
        id: Annotated[int, Path(description="The ID of the book to request.")] # id deve essere compreso tra 1 e 3
    ) -> Book:
    """ Get book by id. """
    try:
        return books[id]
    # se l'id non esiste, solleva un'eccezione
    # raise keyError
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found.")

@router.post("/{id}/review")
def add_review(
    id: Annotated[int, Path(ge=1, le=5)],
    review: Review
):
    """ Add review to book. """
    try:
        books[id].review = review.review
        return "Review successfully added."
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found.")
    except ValidationError:
        raise HTTPException(status_code=400, detail="The review must be between 1 and 5.")

