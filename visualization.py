"""Generate charts for the Book Data Pipeline project.

This script reads data from the existing SQLite database and creates a single
visual report showing price vs rating.

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
    colors = ["#4C72B0" if book["in_stock"] else "#C44E52" for book in books]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(ratings, prices, c=colors, alpha=0.85, edgecolors="black", linewidths=0.5)
    ax.set_title("Price vs Rating Scatter Plot")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Price (£)")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.grid(True, linestyle="--", alpha=0.3)

    ax.legend(
        handles=[
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#4C72B0", markeredgecolor="black", label="In stock", markersize=8),
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#C44E52", markeredgecolor="black", label="Out of stock", markersize=8),
        ],
        loc="best",
        frameon=True,
    )

    fig.tight_layout()

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