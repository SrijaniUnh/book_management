from django.urls import path
from .views import add_book, update_book, delete_book, list_books

urlpatterns = [
    path('add/', add_book, name='add_book'),
    path('update/<int:book_id>/', update_book, name='update_book'),
    path('delete/<int:book_id>/', delete_book, name='delete_book'),
    path('list/', list_books, name='list_books'),
    
]
