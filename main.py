import requests
from bs4 import BeautifulSoup


class UserRegistration:
    def __init__(self):
        self.name = None
        self.age = None
        self.preferred_genres = []

    def register_user(self, name, age, preferred_genres):
        self.name = name
        self.age = age
        self.preferred_genres = preferred_genres
        print("User registration successful.")


class BookRecommendation:
    def __init__(self):
        self.genres = {
            "fiction": [
                "Harry Potter and the Sorcerer's Stone",
                "To Kill a Mockingbird",
                "Pride and Prejudice",
            ],
            "mystery": [
                "And Then There Were None",
                "Gone Girl",
                "The Girl with the Dragon Tattoo",
            ],
            "fantasy": [
                "The Hobbit",
                "A Game of Thrones",
                "The Lord of the Rings",
            ],
        }

    def get_recommendations(self, genre):
        books = self.genres.get(genre.lower())
        if books:
            return books
        else:
            return "No recommendations found for the specified genre."


class UserFeedback:
    def __init__(self):
        self.feedback = {}

    def receive_feedback(self, book, rating):
        self.feedback[book] = rating
        print("Thank you for your feedback!")


class BookDetails:
    def __init__(self):
        self.base_url = "https://www.goodreads.com"

    def get_book_details(self, book):
        search_url = (
            f"{self.base_url}/search/index.xml?key=YOUR_GOODREADS_API_KEY&q={book}"
        )
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, "xml")
        best_book = soup.find("best_book")

        if best_book:
            author = (
                best_book.find("name").text.strip() if best_book.find("name") else "N/A"
            )
            description = (
                best_book.find("description").text.strip()
                if best_book.find("description")
                else "N/A"
            )
            average_rating = (
                best_book.find("average_rating").text.strip()
                if best_book.find("average_rating")
                else "N/A"
            )

            return {
                "Title": book,
                "Author": author,
                "Description": description,
                "Average Rating": average_rating,
            }
        else:
            return "Book details not found."


class LatestReleases:
    def __init__(self):
        self.base_url = "https://api.nytimes.com/svc/books/v3/lists/overview.json"
        self.api_key = "YOUR_NYTIMES_API_KEY"

    def get_latest_releases(self):
        response = requests.get(self.base_url, params={"api-key": self.api_key})
        if response.status_code == 200:
            data = response.json()
            books = [book["title"] for book in data.get("results", {}).get("lists", [])]
            return books
        else:
            return "Failed to retrieve latest releases."


class PopularAuthors:
    def __init__(self):
        self.base_url = "https://www.goodreads.com/author/featured"
        self.api_key = "YOUR_GOODREADS_API_KEY"

    def get_popular_authors(self):
        author_url = f"{self.base_url}?key={self.api_key}"
        response = requests.get(author_url)
        soup = BeautifulSoup(response.content, "html.parser")

        popular_authors = soup.find_all("img", class_="authorCover")
        authors = [author.get("alt").strip() for author in popular_authors]
        return authors


def main():
    registration = UserRegistration()

    name = "John Doe"
    age = 25
    preferred_genres = ["mystery", "fantasy"]

    registration.register_user(name, age, preferred_genres)

    recommendation = BookRecommendation()
    genre = "fiction"
    recommended_books = recommendation.get_recommendations(genre)
    print("Recommended books:", recommended_books)

    feedback = UserFeedback()
    book = "To Kill a Mockingbird"
    rating = 5
    feedback.receive_feedback(book, rating)

    book_details = BookDetails()
    book_info = book_details.get_book_details(book)
    print("Book details:", book_info)

    releases = LatestReleases()
    latest_books = releases.get_latest_releases()
    print("Latest book releases:", latest_books)

    authors = PopularAuthors()
    popular_authors = authors.get_popular_authors()
    print("Popular authors:", popular_authors)


if __name__ == "__main__":
    main()
