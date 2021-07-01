from django.urls import path
from .views import orders_list, create_order, delete_order, edit_order, not_returned, return_book


urlpatterns = [
    path('', orders_list, name='orders_list'),
    path('not_returned/', not_returned, name='not_returned'),
    path('create/', create_order, name='create_order'),
    path('delete/<int:order_id>', delete_order),
    path('edit/<int:order_id>', edit_order),
    path('return/<int:order_id>', return_book, name='return book'),
]
