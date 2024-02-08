from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bookstore.views import HomeView, AboutView, BookSearchView, create_book, MyBooksView, EditBookView, DeleteBookView

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_my_books_url_resolves(self):
        url = reverse('my_books')
        self.assertEqual(resolve(url).func.view_class, MyBooksView)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func.view_class, AboutView)

    def test_book_search_url_resolves(self):
        url = reverse('book_search')
        self.assertEqual(resolve(url).func.view_class, BookSearchView)

    def test_create_book_url_resolves(self):
        url = reverse('create_book')
        self.assertEqual(resolve(url).func, create_book)

    def test_edit_book_url_resolves(self):
        url = reverse('edit_book', args=['1'])  # Provide a sample primary key '1'
        self.assertEqual(resolve(url).func.view_class, EditBookView)

    def test_delete_book_url_resolves(self):
        url = reverse('delete_book', args=['1'])  # Provide a sample primary key '1'
        self.assertEqual(resolve(url).func.view_class, DeleteBookView)
