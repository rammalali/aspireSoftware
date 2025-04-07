from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None  # NEW

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    year: Optional[int]
    genre: Optional[str]
    isbn: Optional[str]
    available: Optional[bool]

class BookOut(BookCreate):
    id: UUID
    available: bool

    class Config:
        orm_mode = True
