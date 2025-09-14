import mysql.connector
from datetime import date

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # <-- apna MySQL username
        password="SHahrukh@123",     # <-- apna MySQL password
        database="library_db"
    )

# Add a new book
def add_book():
    conn = connect_db()
    cursor = conn.cursor()
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    quantity = int(input("Enter quantity: "))
    sql = "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (title, author, quantity))
    conn.commit()
    print("Book added successfully!")
    cursor.close()
    conn.close()

# View all books
def view_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\nBooks in Library:")
    print("ID | Title | Author | Quantity")
    for book in books:
        print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
    cursor.close()
    conn.close()

# Search book by title or author
def search_books():
    conn = connect_db()
    cursor = conn.cursor()
    keyword = input("Enter title or author to search: ")
    sql = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
    cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    if results:
        print("Search Results:")
        print("ID | Title | Author | Quantity")
        for book in results:
            print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
    else:
        print("No books found.")
    cursor.close()
    conn.close()

# Issue a book
def issue_book():
    conn = connect_db()
    cursor = conn.cursor()
    book_id = int(input("Enter book ID to issue: "))
    issued_to = input("Enter name of the person: ")

    cursor.execute("SELECT quantity FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        sql_issue = "INSERT INTO issued_books (book_id, issued_to, issue_date) VALUES (%s, %s, %s)"
        cursor.execute(sql_issue, (book_id, issued_to, date.today()))
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Book not available or invalid book ID.")
    cursor.close()
    conn.close()

# Return a book
def return_book():
    conn = connect_db()
    cursor = conn.cursor()
    issue_id = int(input("Enter issue ID to return: "))

    cursor.execute("SELECT book_id, return_date FROM issued_books WHERE issue_id = %s", (issue_id,))
    result = cursor.fetchone()
    if result:
        book_id, return_date_val = result
        if return_date_val is None:
            cursor.execute("UPDATE issued_books SET return_date = %s WHERE issue_id = %s", (date.today(), issue_id))
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
            conn.commit()
            print("Book returned successfully!")
        else:
            print("This book has already been returned.")
    else:
        print("Invalid issue ID.")
    cursor.close()
    conn.close()

# View issued books
def view_issued_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ib.issue_id, b.title, ib.issued_to, ib.issue_date, ib.return_date
        FROM issued_books ib
        JOIN books b ON ib.book_id = b.book_id
    """)
    issued = cursor.fetchall()
    print("\nIssued Books:")
    print("Issue ID | Title | Issued To | Issue Date | Return Date")
    for row in issued:
        return_date = row[4] if row[4] else "Not returned"
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {return_date}")
    cursor.close()
    conn.close()

# Main menu
def main():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Books")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Issued Books")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_books()
        elif choice == '4':
            issue_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            view_issued_books()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

