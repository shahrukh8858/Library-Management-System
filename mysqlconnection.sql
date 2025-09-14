-- Agar purana database already bana hai to delete kar do (testing ke liye)
DROP DATABASE IF EXISTS library_db;

-- Step 1: Naya database banao
CREATE DATABASE library_db;

-- Step 2: Database use karo
USE library_db;

-- Step 3: Books table banao
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    quantity INT NOT NULL
);

-- Step 4: Issued Books table banao
CREATE TABLE issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    issued_to VARCHAR(255) NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);
SELECT * FROM books;
-- Saari books delete karna
-- Books table me se book delete karna (book_id ke basis par)
DELETE FROM books WHERE book_id = 2;
select *
from books;
