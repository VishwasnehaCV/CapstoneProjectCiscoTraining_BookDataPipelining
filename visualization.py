"""Generate charts for the Book Data Pipeline project.

This script reads data from the existing SQLite database and creates a small
visual report covering rating distribution, stock status, and price spread.

Examples:
    python visualization.py
    python visualization.py --output books_dashboard.png --show
    python visualization.py --csv-output exported_books.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from database import BookDatabaseManager


DEFAULT_OUTPUT = "books_dashboard.png"
DEFAULT_CSV_OUTPUT = "exported_books.csv"


def load_books() -> list[dict]:
    """Fetch all books from the SQLite database."""
    db = BookDatabaseManager()
    return db.get_books()


def export_books_to_csv(books: list[dict], csv_output_path: str) -> None:
    """Export the current book rows to a CSV file."""
    if not books:
        raise ValueError("No books found in the database. Run load_data.py first.")

    output_file = Path(csv_output_path)
    with output_file.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(
            file_handle,
            fieldnames=["id", "title", "price", "in_stock", "rating"],
        )
        writer.writeheader()
        writer.writerows(books)


def build_dashboard(books: list[dict], output_path: str, show: bool = False) -> None:
    """Create and save the visualization dashboard."""
    if not books:
        raise ValueError("No books found in the database. Run load_data.py first.")

    prices = [float(book["price"]) for book in books]
    ratings = [int(book["rating"]) for book in books]
    in_stock_count = sum(1 for book in books if book["in_stock"])
    out_of_stock_count = len(books) - in_stock_count

    rating_counts = {rating: ratings.count(rating) for rating in range(1, 6)}

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Book Data Pipeline Dashboard", fontsize=18, fontweight="bold")

    axes[0, 0].bar(rating_counts.keys(), rating_counts.values(), color="#4C72B0")
    axes[0, 0].set_title("Books by Rating")
    axes[0, 0].set_xlabel("Rating")
    axes[0, 0].set_ylabel("Count")
    axes[0, 0].set_xticks([1, 2, 3, 4, 5])

    axes[0, 1].pie(
        [in_stock_count, out_of_stock_count],
        labels=["In stock", "Out of stock"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#55A868", "#C44E52"],
    )
    axes[0, 1].set_title("Stock Status")

    axes[1, 0].hist(prices, bins=min(10, len(prices)), color="#8172B2", edgecolor="black")
    axes[1, 0].set_title("Price Distribution")
    axes[1, 0].set_xlabel("Price (£)")
    axes[1, 0].set_ylabel("Number of Books")

    axes[1, 1].axis("off")
    summary_text = (
        f"Total books: {len(books)}\n"
        f"In stock: {in_stock_count}\n"
        f"Out of stock: {out_of_stock_count}\n"
        f"Average price: £{sum(prices) / len(prices):.2f}\n"
        f"Highest price: £{max(prices):.2f}\n"
        f"Lowest price: £{min(prices):.2f}"
    )
    axes[1, 1].text(
        0.05,
        0.95,
        summary_text,
        va="top",
        ha="left",
        fontsize=12,
        bbox={"facecolor": "white", "edgecolor": "gray", "boxstyle": "round,pad=0.5"},
    )
    axes[1, 1].set_title("Summary")

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    output_file = Path(output_path)
    fig.savefig(output_file, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create charts for the book database")
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output image path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--csv-output",
        default=DEFAULT_CSV_OUTPUT,
        help=f"CSV export path (default: {DEFAULT_CSV_OUTPUT})",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the dashboard window after saving",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    books = load_books()
    export_books_to_csv(books, args.csv_output)
    build_dashboard(books, args.output, show=args.show)
    print(f"CSV exported to {args.csv_output}")
    print(f"Dashboard saved to {args.output}")


if __name__ == "__main__":
    main()