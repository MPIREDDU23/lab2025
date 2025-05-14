#!/opt/homebrew/bin/python3

from models.book import Book 

books = {
    1: Book(id=1, title="titolo", author="autore", review=5),
    2: Book(id=2, title="titolo2", author="autore2", review=4),
    3: Book(id=3, title="titolo3", author="autore3", review=3),
}