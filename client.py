"""Command-line client for the Book Data Pipeline API.

Use this script to exercise the FastAPI app from the terminal:

    python client.py list
    python client.py get 1
    python client.py create
    python client.py update 1
    python client.py delete 1

The default API base URL is http://127.0.0.1:8000.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

import requests


DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def request_json(method: str, url: str, payload: dict[str, Any] | None = None):
    response = requests.request(method, url, json=payload, timeout=10)
    response.raise_for_status()

    if response.status_code == 204:
        return None

    return response.json()


def print_book(book: dict[str, Any]) -> None:
    print(
        f"#{book['id']} | {book['title']} | £{book['price']:.2f} | "
        f"{'In stock' if book['in_stock'] else 'Out of stock'} | Rating {book['rating']}"
    )


def print_books(books: list[dict[str, Any]]) -> None:
    if not books:
        print("No books found.")
        return

    for book in books:
        print_book(book)


def prompt_book_data() -> dict[str, Any]:
    title = input("Title: ").strip()
    price = float(input("Price: ").strip())
    in_stock_input = input("In stock? (y/n): ").strip().lower()
    rating = int(input("Rating (1-5): ").strip())

    return {
        "title": title,
        "price": price,
        "in_stock": in_stock_input in {"y", "yes", "true", "1"},
        "rating": rating,
    }


def list_books(base_url: str) -> None:
    books = request_json("GET", f"{base_url}/books")
    print_books(books)


def get_book(base_url: str, book_id: int) -> None:
    book = request_json("GET", f"{base_url}/books/{book_id}")
    print(json.dumps(book, indent=2))


def create_book(base_url: str) -> None:
    payload = prompt_book_data()
    book = request_json("POST", f"{base_url}/books", payload)
    print("Created book:")
    print(json.dumps(book, indent=2))


def update_book(base_url: str, book_id: int) -> None:
    payload = prompt_book_data()
    book = request_json("PUT", f"{base_url}/books/{book_id}", payload)
    print("Updated book:")
    print(json.dumps(book, indent=2))


def delete_book(base_url: str, book_id: int) -> None:
    request_json("DELETE", f"{base_url}/books/{book_id}")
    print(f"Deleted book #{book_id}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Book Data Pipeline API client")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base URL (default: {DEFAULT_BASE_URL})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all books")

    get_parser = subparsers.add_parser("get", help="Get one book by id")
    get_parser.add_argument("book_id", type=int)

    subparsers.add_parser("create", help="Create a new book")

    update_parser = subparsers.add_parser("update", help="Update an existing book")
    update_parser.add_argument("book_id", type=int)

    delete_parser = subparsers.add_parser("delete", help="Delete a book")
    delete_parser.add_argument("book_id", type=int)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "list":
            list_books(args.base_url)
        elif args.command == "get":
            get_book(args.base_url, args.book_id)
        elif args.command == "create":
            create_book(args.base_url)
        elif args.command == "update":
            update_book(args.base_url, args.book_id)
        elif args.command == "delete":
            delete_book(args.base_url, args.book_id)
    except requests.HTTPError as exc:
        response = exc.response
        detail = response.text if response is not None else str(exc)
        print(f"Request failed: {detail}")
    except requests.RequestException as exc:
        print(f"Network error: {exc}")


if __name__ == "__main__":
    main()