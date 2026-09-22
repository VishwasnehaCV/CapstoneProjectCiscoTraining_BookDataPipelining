from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import BookDatabaseManager
app = FastAPI(
    title="Book Data Pipeline API",
    description="CRUD REST API for scraped book data",
    version="1.0.0",
)
db = BookDatabaseManager()

class Book(BaseModel):
    title: str
    price: float = Field(ge=0)
    in_stock: bool
    rating: int = Field(ge=1, le=5)

class BookResponse(Book):
    id: int

@app.get("/")
def home():
    return {"message": "Book Data Pipeline API is running"}

@app.get("/books", response_model=list[BookResponse])
def get_books():
    return db.get_books()

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = db.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: Book):
    book_id = db.create_book(
        title=book.title,
        price=book.price,
        in_stock=book.in_stock,
        rating=book.rating,
    )
    return {**book.model_dump(), "id": book_id}

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: Book):
    updated = db.update_book(
        book_id=book_id,
        title=book.title,
        price=book.price,
        in_stock=book.in_stock,
        rating=book.rating,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return {**book.model_dump(), "id": book_id}

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    deleted = db.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

