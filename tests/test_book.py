from library_system.book import Book


def test_book_attributes():
    book = Book("B001", "Python Basics", "Alice")
    assert book.book_id == "B001"
    assert book.title == "Python Basics"
    assert book.author == "Alice"
    assert book.available is True
