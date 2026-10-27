from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from database import get_books_from_db,create_book_in_db,get_book_from_db,update_book_in_db,delete_book_from_db

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None

@app.get("/books")
def get_books():
    return get_books_from_db()

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    return create_book_in_db(book)

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = get_book_from_db(book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.patch("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    update_data = book_update.model_dump(exclude_unset=True, exclude_none=True)
    book = update_book_in_db(book_id, update_data)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted = delete_book_from_db(book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}

