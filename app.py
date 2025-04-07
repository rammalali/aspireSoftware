# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.models import Book, Base
from backend.schemas import BookCreate, BookUpdate, BookOut
from backend.my_database import get_db, engine

from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy import or_
from backend.ai_utils import generate_book_description, generate_embedding


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Runs on shutdown (optional)
    # await engine.dispose()


app = FastAPI(lifespan=lifespan)

@app.post("/books/", response_model=BookOut)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    book_data = book.dict()

    if not book_data.get("genre"):
        book_data["genre"] = "general"
    if not book_data.get("isbn"):
        book_data["isbn"] = "000-0000000000"

    # Generate description if missing
    if not book_data.get("description"):
        book_data["description"] = await generate_book_description(
            title=book.title,
            author=book.author,
            genre=book_data["genre"]
        )

    # Generate embedding
    embedding = await generate_embedding(book_data["description"])
    book_data["embedding"] = embedding

    new_book = Book(**book_data)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


@app.get("/books/", response_model=list[BookOut])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return result.scalars().all()


@app.get("/books/{book_id}", response_model=BookOut)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=BookOut)
async def update_book(book_id: UUID, updates: BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)
    return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.delete(book)
    await db.commit()
    return {"detail": "Book deleted successfully"}


@app.post("/books/{book_id}/checkout", response_model=BookOut, status_code=status.HTTP_200_OK)
async def checkout_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is already checked out")

    book.available = False
    await db.commit()
    await db.refresh(book)
    return book


@app.post("/books/{book_id}/checkin", response_model=BookOut, status_code=status.HTTP_200_OK)
async def checkin_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available:
        raise HTTPException(status_code=400, detail="Book is already checked in")

    book.available = True
    await db.commit()
    await db.refresh(book)
    return book



@app.get("/books/search", response_model=list[BookOut])
async def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    isbn: Optional[str] = None,
    year: Optional[int] = None,
    available: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Book)

    if title:
        query = query.where(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))
    if genre:
        query = query.where(Book.genre.ilike(f"%{genre}%"))
    if isbn:
        query = query.where(Book.isbn.ilike(f"%{isbn}%"))
    if year:
        query = query.where(Book.year == year)
    if available is not None:
        query = query.where(Book.available == available)

    result = await db.execute(query)
    return result.scalars().all()
