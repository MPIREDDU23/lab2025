#!/Users/marcopireddu/miniconda3/envs/pw/bin/python

from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from faker import Faker
import os
from models.book import Book
from models.user import User
from models.book_user_link import BookUserLink as BUL

sqlite_file_name = "app/data/database.db" # SQLite database file name
sqlite_url = f"sqlite:///{sqlite_file_name}" # SQLite URL format
connect_args = {"check_same_thread": False} # SQLite connection arguments
echo_mode = True # Set to True to see SQL queries in the console
# Create the SQLAlchemy engine
engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
    echo=echo_mode
)

def init_database():
    ds_exists = os.path.exists(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker()
        with Session(engine) as session:
            for i in range(10):
                user = User(
                    name = f.name(),
                    birth_date= f.date_of_birth(minimum_age=18, maximum_age=80),
                    city = f.city()
                )
                session.add(user)
            session.commit()
            for i in range(10):
                book = Book(
                    title=f.sentence(),
                    author=f.name(),
                    review=f.pyint(min_value=0, max_value=5),
                )
                session.add(book)
            for i in range(10):
                try:
                    book_user_link = BUL(
                        user_id=f.pyint(min_value=1, max_value=10),
                        book_id=f.pyint(min_value=1, max_value=10)
                    )
                    session.add(book_user_link)
                except Exception as e:
                    continue
            session.commit()
    # Create the database and tables if they don't exist

def get_session():
    # Create a new session for database operations
    with Session(engine) as session:
        yield session
        # Automatically close the session after use

SessionDep = Annotated[Session, Depends(get_session)]