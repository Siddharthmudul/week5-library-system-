class Book:
    """Represents a book in the library."""

    def __init__(
        self,
        title,
        author,
        isbn,
        year,
        available=True,
        borrowed_by=None,
        due_date=None
    ):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = available
        self.borrowed_by = borrowed_by
        self.due_date = due_date

    def check_out(self, member_id, due_date):
        """Borrow the book."""

        if not self.available:
            return False

        self.available = False
        self.borrowed_by = member_id
        self.due_date = due_date

        return True

    def return_book(self):
        """Return the book."""

        if self.available:
            return False

        self.available = True
        self.borrowed_by = None
        self.due_date = None

        return True

    def get_status(self):
        """Return readable book status."""

        if self.available:
            return "Available"

        return (
            f"Borrowed by {self.borrowed_by} "
            f"(Due: {self.due_date})"
        )

    def __str__(self):
        return (
            f"{self.title}\n"
            f"Author: {self.author}\n"
            f"ISBN: {self.isbn}\n"
            f"Year: {self.year}\n"
            f"Status: {self.get_status()}"
        )

    def to_dict(self):
        """Convert object to dictionary."""

        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "available": self.available,
            "borrowed_by": self.borrowed_by,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        """Create Book object from dictionary."""

        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            year=data["year"],
            available=data.get("available", True),
            borrowed_by=data.get("borrowed_by"),
            due_date=data.get("due_date")
        )