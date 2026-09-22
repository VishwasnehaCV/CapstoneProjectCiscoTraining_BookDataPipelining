from scraper import BookScraper
from database import BookDatabaseManager

def load_scraped_books():
    scraper = BookScraper()
    db_manager = BookDatabaseManager()

    books = scraper.scrape_books()
    for book in books:
        db_manager.create_book(
            title=book["title"],
            price=book["price"],
            in_stock=book["in_stock"],
            rating=book["rating"]
        )

if __name__ == "__main__":
    load_scraped_books()



    