from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.read, name="books_list"),
    path("create", views.create, name="create_book"),
    path("delete/<book_id>/", views.delete, name="delete"),
    path("edit/<book_id>/", views.edit, name="edit")
]
