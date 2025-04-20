from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
]
