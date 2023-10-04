import requests
from bs4 import BeautifulSoup

class HttpRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

class UserRegistration:
    """Handles user registration including name, age, and preferred genres."""
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
    """Provides book recommendations based on genre."""
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
    """Collects and stores user feedback on books."""
    def __init__(self):
        self.feedback = {}

    def receive_feedback(self, book, rating):
        self.feedback[book] = rating
        print("Thank you for your feedback!")

class BookDetails(HttpRequest):
    """Fetches book details from Goodreads."""
    def __init__(self, api_key):
        super().__init__("https://www.goodreads.com")
        self.api_key = api_key

    def get_book_details(self, book):
        response = self.get(
            "/search/index.xml",
            params={"key": self.api_key, "q": book}
        )

        if response:
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
        else:
            return "Failed to retrieve book details."

class LatestReleases(HttpRequest):
    """Fetches the latest book releases from NYTimes."""
    def __init__(self, api_key):
        super().__init__("https://api.nytimes.com/svc/books/v3/lists/overview.json")
        self.api_key = api_key

    def get_latest_releases(self):
        response = self.get("", params={"api-key": self.api_key})
        if response:
            data = response.json()
            books = [book["title"] for book in data.get("results", {}).get("lists", [])]
            return books
        else:
            return "Failed to retrieve latest releases."

class PopularAuthors(HttpRequest):
    """Fetches popular authors from Goodreads."""
    def __init__(self, api_key):
        super().__init__("https://www.goodreads.com/author/featured")
        self.api_key = api_key

    def get_popular_authors(self):
        response = self.get("", params={"key": self.api_key})
        if response:
            soup = BeautifulSoup(response.content, "html.parser")
            popular_authors = soup.find_all("img", class_="authorCover")
            authors = [author.get("alt").strip() for author in popular_authors]
            return authors
        else:
            return "Failed to retrieve popular authors."

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

    book_details = BookDetails(api_key="YOUR_GOODREADS_API_KEY")
    book_info = book_details.get_book_details(book)
    print("Book details:", book_info)

    releases = LatestReleases(api_key="YOUR_NYTIMES_API_KEY")
    latest_books = releases.get_latest_releases()
    print("Latest book releases:", latest_books)

    authors = PopularAuthors(api_key="YOUR_GOODREADS_API_KEY")
    popular_authors = authors.get_popular_authors()
    print("Popular authors:", popular_authors)

if __name__ == "__main__":
    main()
