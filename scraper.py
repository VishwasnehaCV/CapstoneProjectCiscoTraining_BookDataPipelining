# import requests
# from bs4 import BeautifulSoup
# url = "https://books.toscrape.com/"
# response = requests.get(url)
# print(response.status_code)

# soup = BeautifulSoup(response.text, "html.parser")

# books = soup.select("article.product_pod")[:20]

# print("number of books found:", len(books))


# first_book = books[0]
# title=first_book.select_one("h3 a")["title"]

# print("title:", title)

# price_text=first_book.select_one(".price_color").get_text(strip=True)
# print("price:", price_text)

# price = float(price_text.replace("£", "").replace("Â", ""))  # Remove the currency symbol and convert to float
# print("price as float:", price)


# availability_text=first_book.select_one(".availability").get_text(" ",strip=True)
# print("availability:", availability_text)

# in_stock = "In stock" in availability_text
# print("in stock:", in_stock)


# rating_map = {
#     "One": 1,
#     "Two": 2,
#     "Three": 3,
#     "Four": 4,
#     "Five": 5
# }
# rating_element = first_book.select_one("p.star-rating")
# rating_classes=rating_element.get("class",[])
# print("rating classes:", rating_classes)
# rating = 0

# for class_name in rating_classes:
#     if class_name in rating_map:
#         rating = rating_map[class_name]
#         break

# print("Rating:", rating)



import requests
from bs4 import BeautifulSoup


class BookScraper:
    """Scrape book data from books.toscrape.com."""

    def __init__(self, url="https://books.toscrape.com/"):
        self.url = url
        self.rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }

    def scrape_books(self, limit=20):
        response = requests.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")[:limit]

        book_data = []

        for book in books:
            title = book.select_one("h3 a")["title"].strip()

            price_text = book.select_one(".price_color").get_text(strip=True)
            price = float(price_text.replace("£", "").replace("Â", ""))

            availability = book.select_one(".availability").get_text(" ", strip=True)
            in_stock = "In stock" in availability

            rating_element = book.select_one("p.star-rating")
            rating = 0

            for class_name in rating_element.get("class", []):
                if class_name in self.rating_map:
                    rating = self.rating_map[class_name]
                    break

            book_data.append(
                {
                    "title": title,
                    "price": price,
                    "in_stock": in_stock,
                    "rating": rating,
                }
            )

        return book_data


if __name__ == "__main__":
    scraper = BookScraper()
    books = scraper.scrape_books()
    print("Total books scraped:", len(books))
    for book in books:
        print(book)