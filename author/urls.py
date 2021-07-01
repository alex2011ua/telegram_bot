from django.urls import path
from . import views

urlpatterns = [
    path("", views.showlist, name="authors_list"),
    path("create", views.create, name="create_author"),
    path("delete/<author_id>/", views.delete, name="delete"),
    path("update/<author_id>", views.edit, name="edit")


]