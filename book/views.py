from django.shortcuts import render, redirect

from .models import Book
# Create your views here.

def book_list(request):
    context = {}
    all_book = Book.get_all()
    context.update({'all_book': all_book})
    return render(request, 'book/all_book.html', context)


def book_form(request, id = 0):
    if request.method == 'GET':
        if id == 0:
            return render(request, 'book/book_form.html')
        else:
            book = Book.get_by_id(id)
            context = {'book': book}
            return render(request, 'book/book_form.html', context)
    else:
        if id == 0:
            name = (request.POST.get('name'))
            decsription = (request.POST.get('description'))
            count = (request.POST.get('count'))
            b = Book.create(name, decsription, int(count))
            return redirect('book:book_list')
        else:
            name = (request.POST.get('name'))
            decsription = (request.POST.get('description'))
            count = (request.POST.get('count'))
            book = Book.get_by_id(id)
            book.update(name, decsription, count)
            return redirect('book:book_list')

def book_delete(request, id):
    Book.delete_by_id(id)
    return redirect('book:book_list')