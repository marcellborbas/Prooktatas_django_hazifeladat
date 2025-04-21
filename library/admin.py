from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from .models import Book, Author


class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


# A kiadás éve filter
class PublicationYearFilter(admin.SimpleListFilter):
    title = 'Publication Year'
    parameter_name = 'publication_year'

    def lookups(self, request, model_admin):
        return [
            ('before_2023', 'Before 2023'),
            ('2023_2024', '2023–2024'),
            ('after_2025', 'After 2025'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'before_2023':
            return queryset.filter(publication_year__lt=2023)
        elif value == '2023_2025':
            return queryset.filter(publication_year__gte=2023, publication_year__lte=2025)
        elif value == 'after_2025':
            return queryset.filter(publication_year__gt=2025)
        return queryset

@admin.action(description='Kikölcsönzés (nem elérhető)')
def mark_as_borrowed(modeladmin, request, queryset):
    queryset.update(available=False)

@admin.action(description='Visszavétel (elérhető)')
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(available=True)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_year', 'display_authors', 'available', 'borrowed_by_name')
    inlines = [AuthorInline]
    exclude = ('authors',)
    list_filter = [PublicationYearFilter]
    actions = [mark_as_borrowed, mark_as_returned]

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    def borrowed_by_name(self, obj):
        return obj.borrowed_by.username if obj.borrowed_by else 'Not borrowed'

    borrowed_by_name.short_description = 'Borrowed By'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'nationality', 'get_books_count')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('nationality',('birth_date', DateRangeFilter))

    def get_books_count(self, obj):
        return obj.books.count()  # Updated to use the related_name

    get_books_count.short_description = 'Books Count'
