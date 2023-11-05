from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import AddBookForm, UpdateBookForm
from .external_api import fetch_book_details

def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            additional_details = fetch_book_details(book.title, book.author)
            book.summary = additional_details.get('summary', '')
            book.cover_url = additional_details.get('cover_url', '')
            book.save()
            return redirect('list_books')
    else:
        form = AddBookForm()

    return render(request, 'bookstore/add_book.html', {'form': form})