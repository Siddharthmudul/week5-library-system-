import json
import os
import shutil

from datetime import datetime, timedelta

from .book import Book
from .member import Member


MAX_BORROW_DAYS = 14
FINE_PER_DAY = 2.0


class Library:
    """Main library management system."""

    def __init__(
        self,
        books_file="data/books.json",
        members_file="data/members.json",
        backup_dir="data/backup"
    ):
        self.books = {}
        self.members = {}

        self.books_file = books_file
        self.members_file = members_file
        self.backup_dir = backup_dir

        self.create_data_directories()

    # ========================================================
    # FILE MANAGEMENT
    # ========================================================

    def create_data_directories(self):
        """Create data directories and files."""

        os.makedirs(
            os.path.dirname(self.books_file),
            exist_ok=True
        )

        os.makedirs(
            os.path.dirname(self.members_file),
            exist_ok=True
        )

        os.makedirs(
            self.backup_dir,
            exist_ok=True
        )

        if not os.path.exists(self.books_file):
            self.write_json(
                self.books_file,
                {}
            )

        if not os.path.exists(self.members_file):
            self.write_json(
                self.members_file,
                {}
            )

    @staticmethod
    def write_json(filename, data):
        """Write data to JSON."""

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

    @staticmethod
    def read_json(filename):
        """Read JSON file."""

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    # ========================================================
    # BOOK MANAGEMENT
    # ========================================================

    def add_book(self, book):
        """Add a new book."""

        if book.isbn in self.books:
            return False

        self.books[book.isbn] = book

        return True

    def find_book(self, isbn):
        """Find book by ISBN."""

        return self.books.get(isbn)

    def remove_book(self, isbn):
        """Remove a book."""

        if isbn not in self.books:
            return False

        book = self.books[isbn]

        if not book.available:
            return False

        del self.books[isbn]

        return True

    # ========================================================
    # MEMBER MANAGEMENT
    # ========================================================

    def register_member(self, member):
        """Register new member."""

        if member.member_id in self.members:
            return False

        self.members[member.member_id] = member

        return True

    def find_member(self, member_id):
        """Find member."""

        return self.members.get(member_id)

    # ========================================================
    # BORROW BOOK
    # ========================================================

    def borrow_book(self, isbn, member_id):
        """Borrow a book."""

        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if book is None:
            return False, "Book not found."

        if member is None:
            return False, "Member not found."

        if not book.available:
            return False, "Book is already borrowed."

        if not member.can_borrow():
            return (
                False,
                "Member has reached the "
                "maximum borrow limit of 5 books."
            )

        today = datetime.now().date()

        due_date = (
            today +
            timedelta(days=MAX_BORROW_DAYS)
        )

        due_date_string = due_date.strftime(
            "%Y-%m-%d"
        )

        book.check_out(
            member_id,
            due_date_string
        )

        member.borrow_book(isbn)

        return True, due_date_string

    # ========================================================
    # RETURN BOOK
    # ========================================================

    def return_book(self, isbn, member_id):
        """Return a book."""

        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if book is None:
            return False, "Book not found.", 0

        if member is None:
            return False, "Member not found.", 0

        if isbn not in member.borrowed_books:
            return (
                False,
                "This member did not borrow this book.",
                0
            )

        overdue_days = 0
        fine = 0

        if book.due_date:

            due_date = datetime.strptime(
                book.due_date,
                "%Y-%m-%d"
            ).date()

            today = datetime.now().date()

            if today > due_date:
                overdue_days = (
                    today - due_date
                ).days

                fine = (
                    overdue_days *
                    FINE_PER_DAY
                )

        book.return_book()

        member.return_book(isbn)

        return True, "Book returned successfully.", fine

    # ========================================================
    # SEARCH BY TITLE
    # ========================================================

    def search_by_title(self, title):
        """Search books by title."""

        title = title.lower().strip()

        results = []

        for book in self.books.values():

            if title in book.title.lower():
                results.append(book)

        return results

    # ========================================================
    # SEARCH BY AUTHOR
    # ========================================================

    def search_by_author(self, author):
        """Search books by author."""

        author = author.lower().strip()

        results = []

        for book in self.books.values():

            if author in book.author.lower():
                results.append(book)

        return results

    # ========================================================
    # SEARCH BY ISBN
    # ========================================================

    def search_by_isbn(self, isbn):
        """Search by ISBN."""

        isbn = isbn.strip()

        book = self.books.get(isbn)

        if book:
            return [book]

        return []

    # ========================================================
    # AVAILABLE BOOKS
    # ========================================================

    def get_available_books(self):
        """Return all available books."""

        return [
            book
            for book in self.books.values()
            if book.available
        ]

    # ========================================================
    # OVERDUE BOOKS
    # ========================================================

    def get_overdue_books(self):
        """Return all overdue books."""

        overdue_books = []

        today = datetime.now().date()

        for book in self.books.values():

            if not book.available and book.due_date:

                due_date = datetime.strptime(
                    book.due_date,
                    "%Y-%m-%d"
                ).date()

                if today > due_date:
                    overdue_books.append(book)

        return overdue_books

    # ========================================================
    # STATISTICS
    # ========================================================

    def get_statistics(self):
        """Return library statistics."""

        total_books = len(self.books)

        available_books = len(
            self.get_available_books()
        )

        borrowed_books = (
            total_books -
            available_books
        )

        overdue_books = len(
            self.get_overdue_books()
        )

        total_members = len(self.members)

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "overdue_books": overdue_books,
            "total_members": total_members
        }

    # ========================================================
    # SAVE BOOKS
    # ========================================================

    def save_books(self):
        """Save books to JSON."""

        data = {
            isbn: book.to_dict()
            for isbn, book in self.books.items()
        }

        try:
            self.write_json(
                self.books_file,
                data
            )

            return True

        except OSError:
            return False

    # ========================================================
    # LOAD BOOKS
    # ========================================================

    def load_books(self):
        """Load books from JSON."""

        try:

            data = self.read_json(
                self.books_file
            )

            self.books = {
                isbn: Book.from_dict(book_data)
                for isbn, book_data in data.items()
            }

            return True

        except FileNotFoundError:

            self.books = {}
            return False

        except json.JSONDecodeError:

            print(
                "Error: Invalid books.json file."
            )

            self.books = {}
            return False

        except OSError:

            self.books = {}
            return False

    # ========================================================
    # SAVE MEMBERS
    # ========================================================

    def save_members(self):
        """Save members to JSON."""

        data = {
            member_id: member.to_dict()
            for member_id, member in self.members.items()
        }

        try:

            self.write_json(
                self.members_file,
                data
            )

            return True

        except OSError:
            return False

    # ========================================================
    # LOAD MEMBERS
    # ========================================================

    def load_members(self):
        """Load members from JSON."""

        try:

            data = self.read_json(
                self.members_file
            )

            self.members = {
                member_id: Member.from_dict(member_data)
                for member_id, member_data in data.items()
            }

            return True

        except FileNotFoundError:

            self.members = {}
            return False

        except json.JSONDecodeError:

            print(
                "Error: Invalid members.json file."
            )

            self.members = {}
            return False

        except OSError:

            self.members = {}
            return False

    # ========================================================
    # SAVE ALL
    # ========================================================

    def save_all(self):
        """Save books and members."""

        books_saved = self.save_books()
        members_saved = self.save_members()

        return books_saved and members_saved

    # ========================================================
    # LOAD ALL
    # ========================================================

    def load_all(self):
        """Load books and members."""

        books_loaded = self.load_books()
        members_loaded = self.load_members()

        return books_loaded and members_loaded

    # ========================================================
    # BACKUP
    # ========================================================

    def backup_data(self):
        """Create backup."""

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_folder = os.path.join(
            self.backup_dir,
            timestamp
        )

        try:

            os.makedirs(
                backup_folder,
                exist_ok=True
            )

            if os.path.exists(self.books_file):
                shutil.copy(
                    self.books_file,
                    os.path.join(
                        backup_folder,
                        "books.json"
                    )
                )

            if os.path.exists(self.members_file):
                shutil.copy(
                    self.members_file,
                    os.path.join(
                        backup_folder,
                        "members.json"
                    )
                )

            return True

        except OSError:
            return False