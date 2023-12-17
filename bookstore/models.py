# book_search/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    author = models.CharField(max_length=255)
    publish_date = models.DateField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        app_label = 'bookstore'
