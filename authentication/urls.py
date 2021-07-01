from django.urls import path
from .views import create_user, users_list, delete_user, edit_user


urlpatterns = [
    path('', users_list, name='users_list'),
    path('create/', create_user, name='create_user'),
    path('delete/<int:user_id>', delete_user),
    path('edit/<int:user_id>', edit_user),
]
