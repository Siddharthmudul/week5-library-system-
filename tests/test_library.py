from library_system.book import Book
from library_system.library import Library
from library_system.member import Member


def test_library_adds_items():
    library = Library()
    book = Book("B001", "Python Basics", "Alice")
    member = Member("M001", "John Doe", "john@example.com")

    library.add_book(book)
    library.add_member(member)

    assert library.list_books() == [book]
    assert library.list_members() == [member]
