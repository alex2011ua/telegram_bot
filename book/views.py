from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data

from . import models
from author import models as md

# Create your views here.
from .forms import BookCreationForm
from .models import Book
from .serializers import BookSerializer


def read(request):
    books_list = models.Book.objects.all()
    # book.save()
    return render(request, 'book/read.html', {"books": books_list})


def delete(request, book_id):
    models.Book.objects.filter(id=book_id).delete()
    return redirect("/book/")


def create(request):
    if request.method == 'GET':
        context = {'form': BookCreationForm()}
        return render(request, 'book/create.html', context)
    else:
        try:
            form = BookCreationForm(request.POST)
            new_book = form.save()
            new_book.save()
            return redirect('books_list')
        except ValueError:
            context = {'form': BookCreationForm(), 'error': 'Invalid Data'}
            return render(request, 'book/create.html', context)


def edit(request, book_id):
    book = models.Book.get_by_id(book_id)
    if request.method == "GET":
        form = BookCreationForm(instance=book)
        context = {'form': form}
        return render(request, 'book/update.html', context)
    else:
        form = BookCreationForm(request.POST, instance=book)
        form.save()
        return redirect('books_list')


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, pk=None):
        book = Book.objects.get(id=pk)
        book.delete()
        return Response(data(self.serializer_class(book)), 204)
