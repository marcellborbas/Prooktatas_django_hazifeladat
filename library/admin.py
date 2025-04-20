from django.contrib import admin
from .models import Book, Author


class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_year', 'display_authors')
    inlines = [AuthorInline]
    exclude = ('authors',)  # We'll use the inline instead

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    display_authors.short_description = 'Authors'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'nationality', 'get_books_count')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('nationality',)

    def get_books_count(self, obj):
        return obj.books.count()  # Updated to use the related_name

    get_books_count.short_description = 'Books Count'