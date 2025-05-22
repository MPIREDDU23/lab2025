from fastapi import APIRouter
from data.db import SessionDep
from sqlmodel import select, delete
from models.user import User, UserPublic
from models.book import Book, BookPublic
from models.book_user_link import BookUserLink as BUL

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(
    session: SessionDep,
    sort: bool = False
) -> list[UserPublic]:
    """ Get all users. """
    statement = select(User)
    users = session.exec(statement).all()
    if sort:
        return sorted(users, key=lambda user: user.id)
    return list(users)

@router.get("/{id}/books")
def get_user_books(
    session: SessionDep,
    id: int
) -> list[BookPublic]:
    """ Get all books of the user with the given ID. """
    statement = select(Book).join(BUL).where(BUL.user_id == id)
    books = session.exec(statement).all()
    return list(books)

