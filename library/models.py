from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    death_date = models.DateField(null=True, blank=True)
    death_place = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author', related_name='books')
    publication_year = models.IntegerField()
    page_count = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} by {', '.join(str(author) for author in self.authors.all())}"





