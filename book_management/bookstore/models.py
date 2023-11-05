from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    summary = models.TextField(blank=True)
    cover_url = models.URLField(blank=True)
    rating = models.FloatField(blank=True, null=True)
