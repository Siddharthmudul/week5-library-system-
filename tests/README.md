Library Management System
Project Description
What I Learned
1. OOP Principles: Classes, objects, inheritance, and encapsulation
2. Class Design: How to design classes for real-world systems
3. Class Relationships: Understanding how different classes interact
4. Method Implementation: Creating methods that model real behaviors
5. Data Persistence: Saving and loading object data to files
Features

•	Add, remove, and search for books
•	Register and manage library members
•	Borrow and return books with due dates
•	Track overdue books and calculate fines
•	Search books by title, author, or ISBN
•	Limit maximum books per member
•	Save/Load data to JSON files
•	User-friendly menu interface
•	Comprehensive error handling

How to Run
cd week5-library-system
python -m library_system.main

Code:

from .book import Book
from .member import Member
from .library import Library

# ============================================================
# INPUT VALIDATION
# ============================================================

def get_non_empty_input(message):
    """Get non-empty user input."""

    while True:

        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty.")

def get_year():
    """Get valid year."""

    while True:

        try:

            year = int(
                input("Enter publication year: ")
            )

            if 1000 <= year <= 2026:
                return year

            print("Please enter a valid year.")

        except ValueError:

            print(
                "Please enter numbers only."
            )

# ============================================================
# DISPLAY BOOK
# ============================================================

def display_book(book, number=None):
    """Display one book."""

    if number is not None:
        print(f"{number}. {book.title}")

    else:
        print(book.title)

    print(f"   Author: {book.author}")
    print(f"   ISBN: {book.isbn}")
    print(f"   Year: {book.year}")
    print(f"   Status: {book.get_status()}")

# ============================================================
# ADD BOOK
# ============================================================

def add_book_menu(library):

    print("\n--- ADD NEW BOOK ---")

    title = get_non_empty_input(
        "Enter title: "
    )

    author = get_non_empty_input(
        "Enter author: "
    )

    isbn = get_non_empty_input(
        "Enter ISBN: "
    )

    year = get_year()

    book = Book(
        title,
        author,
        isbn,
        year
    )

    if library.add_book(book):

        print(
            "\nBook added successfully!"
        )

    else:

        print(
            "\nA book with this ISBN "
            "already exists."
        )

# ============================================================
# REGISTER MEMBER
# ============================================================

def register_member_menu(library):

    print("\n--- REGISTER NEW MEMBER ---")

    name = get_non_empty_input(
        "Enter member name: "
    )

    member_id = get_non_empty_input(
        "Enter member ID: "
    )

    member = Member(
        name,
        member_id
    )

    if library.register_member(member):

        print(
            "\nMember registered successfully!"
        )

    else:

        print(
            "\nMember ID already exists."
        )

# ============================================================
# BORROW BOOK
# ============================================================

def borrow_book_menu(library):

    print("\n--- BORROW BOOK ---")

    isbn = get_non_empty_input(
        "Enter ISBN: "
    )

    member_id = get_non_empty_input(
        "Enter member ID: "
    )

    success, message = library.borrow_book(
        isbn,
        member_id
    )

    if success:

        print(
            "\nBook borrowed successfully!"
        )

        print(
            f"Due Date: {message}"
        )

    else:

        print(
            f"\nError: {message}"
        )

# ============================================================
# RETURN BOOK
# ============================================================

def return_book_menu(library):

    print("\n--- RETURN BOOK ---")

    isbn = get_non_empty_input(
        "Enter ISBN: "
    )

    member_id = get_non_empty_input(
        "Enter member ID: "
    )

    success, message, fine = (
        library.return_book(
            isbn,
            member_id
        )
    )

    if success:

        print(
            f"\n{message}"
        )

        if fine > 0:

            print(
                f"Overdue Fine: ₹{fine:.2f}"
            )

        else:

            print(
                "No overdue fine."
            )

    else:

        print(
            f"\nError: {message}"
        )

# ============================================================
# SEARCH BOOKS
# ============================================================

def search_books_menu(library):

    print("\nSearch books by:")

    print("1. Title")
    print("2. Author")
    print("3. ISBN")
    print("4. Show all available books")

    option = input(
        "\nEnter search option: "
    ).strip()

    results = []
    search_text = ""

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    if option == "1":

        search_text = get_non_empty_input(
            "\nEnter title to search: "
        )

        results = library.search_by_title(
            search_text
        )

    # --------------------------------------------------------
    # AUTHOR
    # --------------------------------------------------------

    elif option == "2":

        search_text = get_non_empty_input(
            "\nEnter author to search: "
        )

        results = library.search_by_author(
            search_text
        )

    # --------------------------------------------------------
    # ISBN
    # --------------------------------------------------------

    elif option == "3":

        search_text = get_non_empty_input(
            "\nEnter ISBN to search: "
        )

        results = library.search_by_isbn(
            search_text
        )

    # --------------------------------------------------------
    # AVAILABLE
    # --------------------------------------------------------

    elif option == "4":

        search_text = "available"

        results = (
            library.get_available_books()
        )

    else:

        print(
            "\nInvalid search option."
        )

        return

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print()

    if option == "4":

        print(
            "Available Books:"
        )

    else:

        print(
            f"Search Results for "
            f"'{search_text}':"
        )

    print("-" * 40)

    if not results:

        print(
            "No books found."
        )

        if option != "4":

            print(
                f"\nFound 0 books matching "
                f"'{search_text}'"
            )

        return

    for index, book in enumerate(
        results,
        start=1
    ):

        display_book(
            book,
            index
        )

        print()

    if option != "4":

        print(
            f"Found {len(results)} books "
            f"matching '{search_text}'"
        )

    else:

        print(
            f"Found {len(results)} "
            f"available books"
        )

# ============================================================
# VIEW ALL BOOKS
# ============================================================

def view_all_books(library):

    print("\nAll Books:")
    print("-" * 40)

    if not library.books:

        print(
            "No books available."
        )

        return

    for index, book in enumerate(
        library.books.values(),
        start=1
    ):

        display_book(
            book,
            index
        )

        print()

# ============================================================
# VIEW ALL MEMBERS
# ============================================================

def view_all_members(library):

    print("\nAll Members:")
    print("-" * 40)

    if not library.members:

        print(
            "No members registered."
        )

        return

    for index, member in enumerate(
        library.members.values(),
        start=1
    ):

        print(
            f"{index}. {member.name}"
        )

        print(
            f"   Member ID: "
            f"{member.member_id}"
        )

        print(
            f"   Borrowed Books: "
            f"{len(member.borrowed_books)}"
        )

        print()

# ============================================================
# VIEW OVERDUE BOOKS
# ============================================================

def view_overdue_books(library):

    overdue_books = (
        library.get_overdue_books()
    )

    print("\nOverdue Books:")
    print("-" * 40)

    if not overdue_books:

        print(
            "No overdue books."
        )

        return

    for index, book in enumerate(
        overdue_books,
        start=1
    ):

        display_book(
            book,
            index
        )

        print()

# ============================================================
# MAIN MENU
# ============================================================

def display_menu():

    print("\n")
    print("=" * 32)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("=" * 32)

def main():

    library = Library()

    print("=" * 32)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("=" * 32)

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    if library.load_books():

        print(
            f"Loaded {len(library.books)} "
            f"books from file"
        )

    else:

        print(
            "Loaded 0 books from file"
        )

    if library.load_members():

        print(
            f"Loaded {len(library.members)} "
            f"members from file"
        )

    else:

        print(
            "Loaded 0 members from file"
        )

    # --------------------------------------------------------
    # MENU LOOP
    # --------------------------------------------------------

    while True:

        print()

        print("1. Add New Book")
        print("2. Register New Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Books")
        print("6. View All Books")
        print("7. View All Members")
        print("8. View Overdue Books")
        print("9. Save & Exit")
        print("0. Exit Without Saving")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # ADD BOOK
        # ----------------------------------------------------

        if choice == "1":

            add_book_menu(library)

        # ----------------------------------------------------
        # REGISTER MEMBER
        # ----------------------------------------------------

        elif choice == "2":

            register_member_menu(library)

        # ----------------------------------------------------
        # BORROW
        # ----------------------------------------------------

        elif choice == "3":

            borrow_book_menu(library)

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        elif choice == "4":

            return_book_menu(library)

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        elif choice == "5":

            search_books_menu(library)

        # ----------------------------------------------------
        # ALL BOOKS
        # ----------------------------------------------------

        elif choice == "6":

            view_all_books(library)

        # ----------------------------------------------------
        # ALL MEMBERS
        # ----------------------------------------------------

        elif choice == "7":

            view_all_members(library)

        # ----------------------------------------------------
        # OVERDUE
        # ----------------------------------------------------

        elif choice == "8":

            view_overdue_books(library)

        # ----------------------------------------------------
        # SAVE AND EXIT
        # ----------------------------------------------------

        elif choice == "9":

            if library.save_all():

                print(
                    "\nData saved successfully."
                )

                print(
                    "Goodbye!"
                )

            else:

                print(
                    "\nError saving data."
                )

            break

        # ----------------------------------------------------
        # EXIT WITHOUT SAVING
        # ----------------------------------------------------

        elif choice == "0":

            print(
                "\nExiting without saving..."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please enter 0-9."
            )

if __name__ == "__main__":
    main()












Output:























































































































































































































































 

 
Testing Evidence

 



 

 

