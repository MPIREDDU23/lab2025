
from sqlmodel import SQLModel, Field
from typing import Annotated

class UserBase(SQLModel):
    name: str
    birth_date: str
    city: str

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    pass