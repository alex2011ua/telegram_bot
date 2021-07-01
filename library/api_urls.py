from django.urls import path, include
from authentication.views_api import UserApiList, UserApiCreate, UserApiDetail, UserApiOrserList
from order.views_api import OrderApiList, OrderApiCreate, OrderApiDetail

urlpatterns = [
    path("user/<int:pk>/order", UserApiOrserList.as_view()),
    path("user/", UserApiList.as_view()),
    path("user/create/", UserApiCreate.as_view()),
    path("user/<int:pk>/", UserApiDetail.as_view()),

    path("order/", OrderApiList.as_view()),
    path("order/create/", OrderApiCreate.as_view()),
    path("order/<int:pk>/", OrderApiDetail.as_view()),

    path('', include('book.book_api_urls')),
    path('', include('author.author_api_urls')),
]
