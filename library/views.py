from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all().order_by('publication_year')  # Könyvek rendezve
    return render(request, 'library/author_detail.html', {
        'author': author,
        'books': books,
        'books_count': books.count()  # Könyvek száma
    })

def index(request):
    return render(request, 'library/index.html')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form, 'book': book})
