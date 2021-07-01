from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data

from . import models
from .forms import AuthorCreationForm
from .serializers import AuthorSerializer


# Create your views here.
from .models import Author


def showlist(request):
    authors_list = models.Author.objects.all()
    print(authors_list)
    #
    return render(request, "author/read.html", {"authors": authors_list})


def create(request):
    if request.method == "GET":
        context = {'form': AuthorCreationForm()}
        return render(request, 'author/create.html', context)
    else:
        try:
            form = AuthorCreationForm(request.POST)
            new_Author = form.save()
            new_Author.save()
            return redirect('authors_list')
        except ValueError:
            context = {'form': AuthorCreationForm(), 'error': 'Invalid Data'}
            return render(request, 'author/create.html', context)


def delete(request, author_id):
    print(author_id)
    models.Author.objects.filter(id=author_id).delete()
    return redirect("authors_list")


def edit(request, author_id):
    author = models.Author.get_by_id(author_id)
    if request.method == "GET":
        form = AuthorCreationForm(instance=author)
        context = {'form': form}
        return render(request, 'author/update.html', context)
    else:
        try:
            form = AuthorCreationForm(request.POST, instance=author)
            form.save()
            return redirect('authors_list')
        except ValueError:
            context = {'form': AuthorCreationForm(), 'error': 'Invalid Data'}
            return render(request, 'author/create.html', context)


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def delete(self, request, pk=None):
        author = Author.objects.get(id=pk)
        author.delete()
        return Response(data(self.serializer_class(author)), 204)

