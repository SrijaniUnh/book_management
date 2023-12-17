from django.urls import path
from .views import HomeView, AboutView, BookSearchView
from .views import create_book, delete_book
from .views import BookSearchView, MyBooksView, EditBookView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my_books/', MyBooksView.as_view(), name='my_books'),
    path('about/', AboutView.as_view(), name='about'),
    path('search/', BookSearchView.as_view(), name='book_search'),
    path('create/', create_book, name='create_book'),
    path('edit/<str:pk>/', EditBookView.as_view(), name='edit_book'),
    path('delete/<str:pk>/', delete_book, name='delete_book'),
    # Add other URL patterns as needed
]
