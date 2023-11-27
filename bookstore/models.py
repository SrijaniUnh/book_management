# book_search/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publish_date = models.DateField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
