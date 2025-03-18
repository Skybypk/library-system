import streamlit as st

# Define Book and User classes
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False

    def check_out(self):
        if self.is_checked_out:
            return f"'{self.title}' is already checked out."
        else:
            self.is_checked_out = True
            return f"'{self.title}' has been checked out."

    def return_book(self):
        if not self.is_checked_out:
            return f"'{self.title}' is not checked out."
        else:
            self.is_checked_out = False
            return f"'{self.title}' has been returned."

    def __str__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.checked_out_books = []

    def check_out_book(self, book):
        if book.is_checked_out:
            return f"'{book.title}' is already checked out."
        else:
            book.check_out()
            self.checked_out_books.append(book)
            return f"'{book.title}' has been checked out by {self.name}."

    def return_book(self, book):
        if book in self.checked_out_books:
            book.return_book()
            self.checked_out_books.remove(book)
            return f"'{book.title}' has been returned by {self.name}."
        else:
            return f"'{book.title}' is not checked out by {self.name}."

    def __str__(self):
        return f"User: {self.name} (ID: {self.user_id})"


# Initialize the library
class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def find_book_by_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def list_books(self):
        if not self.books:
            return "No books in the library."
        return "\n".join(str(book) for book in self.books)

    def list_users(self):
        if not self.users:
            return "No users in the library."
        return "\n".join(str(user) for user in self.users)


# Streamlit App
def main():
    st.title("Library Management System")

    # Initialize session state for library, books, and users
    if "library" not in st.session_state:
        st.session_state.library = Library()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = ["Add Book", "Add User", "Check Out Book", "Return Book", "View Books", "View Users"]
    choice = st.sidebar.selectbox("Choose an action", options)

    if choice == "Add Book":
        st.header("Add a New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        isbn = st.text_input("ISBN")
        if st.button("Add Book"):
            if title and author and isbn:
                book = Book(title, author, isbn)
                st.session_state.library.add_book(book)
                st.success(f"Book '{title}' added successfully!")
            else:
                st.error("Please fill in all fields.")

    elif choice == "Add User":
        st.header("Add a New User")
        name = st.text_input("Name")
        user_id = st.text_input("User ID")
        if st.button("Add User"):
            if name and user_id:
                user = User(name, user_id)
                st.session_state.library.add_user(user)
                st.success(f"User '{name}' added successfully!")
            else:
                st.error("Please fill in all fields.")

    elif choice == "Check Out Book":
        st.header("Check Out a Book")
        user_id = st.text_input("Enter User ID")
        book_title = st.text_input("Enter Book Title")
        if st.button("Check Out"):
            user = st.session_state.library.find_user_by_id(user_id)
            book = st.session_state.library.find_book_by_title(book_title)
            if user and book:
                result = user.check_out_book(book)
                st.success(result)
            else:
                st.error("User or Book not found.")

    elif choice == "Return Book":
        st.header("Return a Book")
        user_id = st.text_input("Enter User ID")
        book_title = st.text_input("Enter Book Title")
        if st.button("Return"):
            user = st.session_state.library.find_user_by_id(user_id)
            book = st.session_state.library.find_book_by_title(book_title)
            if user and book:
                result = user.return_book(book)
                st.success(result)
            else:
                st.error("User or Book not found.")

    elif choice == "View Books":
        st.header("List of Books")
        books_list = st.session_state.library.list_books()
        st.text(books_list)

    elif choice == "View Users":
        st.header("List of Users")
        users_list = st.session_state.library.list_users()
        st.text(users_list)


if __name__ == "__main__":
    main()