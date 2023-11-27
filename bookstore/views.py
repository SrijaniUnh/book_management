# homepage/views.py
import requests
from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Book

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/home.html')

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/about.html')

class BookSearchView(View):
    def get(self, request, *args, **kwargs):
        # Get the search query from the URL parameters
        query = request.GET.get('q')

        if not query:
            # Render the book_search.html template without making an API request
            return render(request, 'bookstore/book_search.html')

        # Define the Open Library API URL
        api_url = f'https://openlibrary.org/search.json?q={query}'

        try:
            # Make a request to the Open Library API
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
        except requests.RequestException as e:
            # Handle API request errors
            return render(request, 'bookstore/book_search.html', {'error': f'Error making API request: {str(e)}'})

        # Extract the list of books from the API response
        books = data.get('docs', [])

        # Extract relevant information for each book
        book_list = []
        for book in books:
            book_info = {
                'title': book.get('title', ''),
                'author': ', '.join(book.get('author_name', [])),
                'publish_date': book.get('publish_date', ''),
                'subject': ', '.join(book.get('subject', [])),
                'cover_url': f'https://covers.openlibrary.org/b/id/{book.get("cover_i", "")}-L.jpg',  # Cover URL
                'isbn': ', '.join(book.get('isbn', [])),
            }
            book_list.append(book_info)

        # Return the list of books as context to be used in the template
        return render(request, 'bookstore/book_search.html', {'books': book_list})
