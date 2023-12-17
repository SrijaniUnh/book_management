# homepage/views.py
import requests
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Book
from .forms import BookForm
from django.utils.dateparse import parse_date
from django import template
from django.http import Http404
from django.http import HttpResponseNotFound
import logging
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log information about the request
        logging.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        # Log information about the response
        logging.info(f"Response: {response.status_code}")
        return response

register = template.Library()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/home.html')

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/about.html')

def create_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')

    return render(request, 'bookstore/create_book.html', {'form': form})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')

class BookSearchView(View):

    my_books = []

    def get(self, request, *args, **kwargs):
        
        query = request.GET.get('q')

        if not query:
            return render(request, 'bookstore/book_search.html')

        api_url = f'https://openlibrary.org/search.json?q={query}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
        except requests.RequestException as e:
            return render(request, 'bookstore/book_search.html', {'error': f'Error making API request: {str(e)}'})

        books = data.get('docs', [])

        book_list = []

        def get_single_value(values):
            """
            Returns the first non-empty value from a list, or None if none are found.
            """
            for value in values:
                if value:
                    return value
                return None
            
        for book in books:
            book_info = {
        'title': book.get('title', ''),
        'author': ', '.join(book.get('author_name', [])),
        'publish_date': get_single_value(book.get('publish_date', [])),
        'subject': get_single_value(book.get('subject', [])),
        'cover_url': f'https://covers.openlibrary.org/b/id/{book.get("cover_i", "")}-L.jpg', 
        'isbn': get_single_value(book.get('isbn', [])),
        }
            book_list.append(book_info)
        
            
        return render(request, 'bookstore/book_search.html', {'books': book_list})

    

    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        author = request.POST.get('author')
        publish_date = request.POST.get('publish_date')
        subject = request.POST.get('subject')
        cover_url = request.POST.get('cover_url')
        isbn = request.POST.get('isbn')

        if title:
            # Add the book to the list
            book = {
            'title': title,
            'author': author,
            'publish_date': publish_date,
            'subject': subject,
            'cover_url': cover_url,
            'isbn': isbn,
            }
            self.my_books.append(book)

        return redirect('my_books')
    
class MyBooksView(View):
    def get(self, request, *args, **kwargs):
        # Access the global my_books list from BookSearchView
        my_books = BookSearchView.my_books
        context = {'my_books': my_books}
        return render(request, 'bookstore/my_books.html', context)

class EditBookView(View):
    def get(self, request, pk, *args, **kwargs):
        book = next((book for book in BookSearchView.my_books if book['title'] == pk), None)

        if not book:
            return HttpResponseNotFound("Book not found in the list")

        form = BookForm(initial=book)
        return render(request, 'bookstore/edit_book.html', {'form': form, 'book': book})
    
    def post(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, title=pk)
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()

            if request.is_ajax():
                return JsonResponse({'success': True})

            return redirect('book_list')  # Redirect to the book list or any other desired page

        if request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors})

        return render(request, 'bookstore/edit_book.html', {'form': form, 'book': book})

    # def post(self, request, pk, *args, **kwargs):
    #     book = next((book for book in BookSearchView.my_books if book['title'] == pk), None)

    #     if not book:
    #         return HttpResponseNotFound("Book not found in the list")

    #     form = BookForm(request.POST)

    #     if form.is_valid():
    #         # Update the book details in the list
    #         book.update(form.cleaned_data)
    #         return redirect('my_books')  # Redirect to the book list or any other desired page

    #     return render(request, 'bookstore/edit_book.html', {'form': form, 'book': book})

    
class DeleteBookView(View):
    @staticmethod
    def delete_book(title, book_list):
        # Find and remove the book from the list based on the title
        for book in book_list:
            if book['title'] == title:
                book_list.remove(book)
                break

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')

        if title:
            # Delete the book from the list
            DeleteBookView.delete_book(title, BookSearchView.my_books)

        # Redirect back to the book search page
        return redirect('book_search')
    