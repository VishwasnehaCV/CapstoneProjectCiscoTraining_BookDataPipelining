import sqlite3


class BookDatabaseManager:
    """SQLite database manager implementing CRUD operations for books."""

    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    in_stock BOOLEAN NOT NULL,
                    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5)
                )
            """)
            conn.commit()

    # CREATE
    def create_book(self, title, price, in_stock, rating):
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO books (title, price, in_stock, rating)
                VALUES (?, ?, ?, ?)
                """,
                (title, price, int(in_stock), rating),
            )
            conn.commit()
            return cursor.lastrowid

    # READ - all
    def get_books(self):
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM books ORDER BY id"
            ).fetchall()
            return [dict(row) for row in rows]

    # READ - one
    def get_book(self, book_id):
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()
            return dict(row) if row else None

    # UPDATE
    def update_book(self, book_id, title, price, in_stock, rating):
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE books
                SET title = ?, price = ?, in_stock = ?, rating = ?
                WHERE id = ?
                """,
                (title, price, int(in_stock), rating, book_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    # DELETE
    def delete_book(self, book_id):
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

    def clear_books(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM books")
            conn.commit()