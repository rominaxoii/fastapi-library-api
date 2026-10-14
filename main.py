from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None

books: dict[int, dict] = {}
next_book_id = 1

@app.get("/books")
def get_books():
    return list(books.values())

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global next_book_id
    new_book = {
        "id": next_book_id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
    }

    books[next_book_id] = new_book
    next_book_id += 1

    return new_book

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=404 , detail="Book not found")
    return book

@app.patch("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404 , detail="Book not found")
    update_data = book_update.model_dump(exclude_unset=True)
    books[book_id].update(update_data)
    return books[book_id]


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
    return {"message": "Book deleted successfully"}

