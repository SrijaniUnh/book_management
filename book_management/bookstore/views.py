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

def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = UpdateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = UpdateBookForm(instance=book)

    return render(request, 'bookstore/update_book.html', {'form': form, 'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('list_books')

    return render(request, 'bookstore/delete_book.html', {'book': book})

def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookstore/list_books.html', {'books': books})