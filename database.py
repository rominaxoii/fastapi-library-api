import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        dbname="library_db",
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        host="localhost",
        port=5432
    )

def get_books_from_db():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, author, year FROM books")
            rows = cursor.fetchall()

            books = []
            for row in rows:
                books.append({
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "year": row[3]
                })

            return books

    finally:
        connection.close()

def create_book_in_db(book):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO books (title, author, year)
                VALUES (%s, %s, %s)
                RETURNING id, title, author, year
                """,
                (book.title, book.author, book.year)
            )

            row = cursor.fetchone()
            connection.commit()

            return {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "year": row[3]
            }

    finally:
        connection.close()

def get_book_from_db(book_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, author, year FROM books WHERE id = %s",
                (book_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "year": row[3]
            }

    finally:
        connection.close()


def update_book_in_db(book_id, update_data):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            if not update_data:
                cursor.execute(
                    "SELECT id, title, author, year FROM books WHERE id = %s",
                    (book_id,)
                )
                row = cursor.fetchone()
            else:
                fields = list(update_data.keys())
                values = list(update_data.values())

                allowed_fields = {"title", "author", "year"}
                
                if not set(fields).issubset(allowed_fields):
                    raise ValueError("Invalid field name")
                
                set_clause = ", ".join(
                    f"{field} = %s" for field in fields
                )

                query = f"""
                    UPDATE books
                    SET {set_clause}
                    WHERE id = %s
                    RETURNING id, title, author, year
                """

                cursor.execute(query, (*values, book_id))
                row = cursor.fetchone()
                connection.commit()

            if row is None:
                return None

            return {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "year": row[3]
            }

    finally:
        connection.close()

def delete_book_from_db(book_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM books
                WHERE id = %s
                RETURNING id
                """,
                (book_id,)
            )

            row = cursor.fetchone()
            connection.commit()

            return row is not None

    finally:
        connection.close()

