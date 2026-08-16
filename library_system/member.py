MAX_BORROW_LIMIT = 5


class Member:
    """Represents a library member."""

    def __init__(
        self,
        name,
        member_id,
        borrowed_books=None
    ):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = borrowed_books or []

    def borrow_book(self, isbn):
        """Add ISBN to borrowed books."""

        if len(self.borrowed_books) >= MAX_BORROW_LIMIT:
            return False

        if isbn in self.borrowed_books:
            return False

        self.borrowed_books.append(isbn)

        return True

    def return_book(self, isbn):
        """Remove ISBN from borrowed books."""

        if isbn not in self.borrowed_books:
            return False

        self.borrowed_books.remove(isbn)

        return True

    def can_borrow(self):
        """Check whether member can borrow more books."""

        return len(self.borrowed_books) < MAX_BORROW_LIMIT

    def to_dict(self):
        """Convert member to dictionary."""

        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member from dictionary."""

        return cls(
            name=data["name"],
            member_id=data["member_id"],
            borrowed_books=data.get(
                "borrowed_books",
                []
            )
        )

    def __str__(self):
        return (
            f"Member ID: {self.member_id}\n"
            f"Name: {self.name}\n"
            f"Borrowed Books: "
            f"{len(self.borrowed_books)}"
        )