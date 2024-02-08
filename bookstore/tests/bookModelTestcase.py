from django.test import TestCase
from bookstore.models import Book
from datetime import date
from django.db.utils import IntegrityError
class BookModelTestCase(TestCase):
    def setUp(self):
        # Create sample data for testing
        Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            publish_date=date(1925, 4, 10),
            subject="Fiction",
            isbn="9780141182636"
        )

        Book.objects.create(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            publish_date=date(1960, 7, 11),
            subject="Classics",
            isbn="9780061120084"
        )

    def test_book_creation(self):
        """Test that books are created with the correct attributes."""
        book1 = Book.objects.get(title="The Great Gatsby")
        self.assertEqual(book1.author, "F. Scott Fitzgerald")
        self.assertEqual(book1.publish_date, date(1925, 4, 10))
        self.assertEqual(book1.subject, "Fiction")
        self.assertEqual(book1.isbn, "9780141182636")

        book2 = Book.objects.get(title="To Kill a Mockingbird")
        self.assertEqual(book2.author, "Harper Lee")
        self.assertEqual(book2.publish_date, date(1960, 7, 11))
        self.assertEqual(book2.subject, "Classics")
        self.assertEqual(book2.isbn, "9780061120084")

    def test_book_update(self):
        """Test updating book attributes."""
        book = Book.objects.get(title="The Great Gatsby")
        book.author = "Updated Author"
        book.subject = "Updated Subject"
        book.save()

        updated_book = Book.objects.get(title="The Great Gatsby")
        self.assertEqual(updated_book.author, "Updated Author")
        self.assertEqual(updated_book.subject, "Updated Subject")

    def test_book_deletion(self):
        """Test deleting a book."""
        book = Book.objects.get(title="To Kill a Mockingbird")
        book.delete()

        with self.assertRaises(Book.DoesNotExist):
            deleted_book = Book.objects.get(title="To Kill a Mockingbird")

    def test_unique_title_constraint(self):
        """Test that titles must be unique."""
        with self.assertRaises(IntegrityError):
            # Attempt to create a book with an existing title
            Book.objects.create(
                title="The Great Gatsby",
                author="Duplicate Author",
                publish_date=date(2000, 1, 1),
                subject="Duplicate Subject",
                isbn="1234567890123"
            )
