# book_search/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publish_date', 'subject']

    # You can customize the form fields if needed, for example, adding widgets or validations.
    # For simplicity, the default fields are used in this example.
