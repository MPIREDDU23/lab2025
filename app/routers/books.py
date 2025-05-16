#!/Users/marcopireddu/miniconda3/envs/pw/bin/python

from fastapi import APIRouter, Request, HTTPException, Path, Form #HTTPException serve per gestire le eccezioni
from models.book import BookCreate, Book, BookPublic
from models.review import Review
from typing import Annotated # Annotated serve per annotare i parametri, definire il tipo di dato e
from pydantic import ValidationError
from fastapi.responses import RedirectResponse
from data.db import SessionDep
from sqlmodel import select

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
    session: SessionDep,
    request: Request,
    sort: bool = False
) -> list[BookPublic]:
    """ Get all books. """
    statement = select(Book)
    books = session.exec(statement).all()
    if sort:
        return sorted(books, key=lambda book: book.id)
    return list(books)

@router.post("/")
def add_book(
    request: Request,
    book: BookCreate,
    session: SessionDep
):
    """ Add a new book. """
    validated_book = Book.model_validate(book)
    session.add(validated_book)
    session.commit()
    return "Book successfully added."

@router.post("_form/")
def add_book_from_form(
    request: Request,
    session: SessionDep,
    book: Annotated[BookCreate, Form()],
    ):
    """ Add a new book from form. """
    validated_book = Book.model_validate(book)
    session.add(validated_book)
    session.commit()
    return "Book successfully added."

@router.delete("/")
def delete_all_books(session: SessionDep):
    """ Delete all books. """
    statement = select(Book)
    session.exec(statement).delete()
    session.commit()
    return "All books successfully deleted."

@router.delete("/{id}")
def delete_book(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to delete.")]
):
    """ Delete the book with the given ID. """
    statement = select(Book).where(Book.id == id)
    # questa get si può fare solo con la chiave primaria
    book = session.get(Book, id)
    # if not book: non è robusto. potrebbe essere restituito un booleanno oltre che None.
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    session.delete(book)
    session.commit()
    return "Book successfully deleted."

@router.put("/{id}")
def update_book(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to update.")],
    newbook: BookCreate
):
    """ Updates the book with the given ID. """
    book = session.get(Book, id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    book.author = newbook.autore
    book.title = newbook.title
    book.review = newbook.review

    session.add(book)
    session.commit()

# /books/{id}
@router.get("/{id}")
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to request.")] # id deve essere compreso tra 1 e 3
    ) -> BookPublic:
    """ Get book by id. """
    # questa get si può fare solo con la chiave primaria
    book = session.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book

@router.post("/{id}/review")
def add_review(
    session: SessionDep,
    id: Annotated[int, Path(ge=1, le=5)],
    review: Review
):
    """ Add review to book. """
    # questa get si può fare solo con la chiave primaria
    book = session.get(Book, id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    book.review = review.review
    session.commit()

    return "Review successfully added."
