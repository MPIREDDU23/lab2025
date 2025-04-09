from pydantic import BaseModel, Field
from typing import Annotated

class Book(BaseModel):
    id: int
    title: str
    author: str
    review: Annotated[int | None, Field(ge=1, le=5)]


book = Book(id=1, title = "titolo", author = "autore", review = 5)
print(book)