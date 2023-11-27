from django.urls import path
from .views import HomeView, AboutView, BookSearchView
from .views import book_list, create_book, edit_book, delete_book

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('search/', BookSearchView.as_view(), name='book_search'),
    path('list/', book_list, name='book_list'),
    path('create/', create_book, name='create_book'),
    path('edit/<int:pk>/', edit_book, name='edit_book'),
    path('delete/<int:pk>/', delete_book, name='delete_book'),
    
    # Add other URL patterns as needed
]
