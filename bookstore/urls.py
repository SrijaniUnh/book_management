from django.urls import path
from .views import HomeView, AboutView, BookSearchView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('search/', BookSearchView.as_view(), name='book_search'),
    
    # Add other URL patterns as needed
]
