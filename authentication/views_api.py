from rest_framework import generics
from .serializers import UserSerializer
from order.serializers import OrderSerializer
from .models import CustomUser
from order.models import Order


class UserApiList(generics.ListAPIView):
    queryset = CustomUser.get_all()
    serializer_class = UserSerializer


class UserApiCreate(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserApiDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserApiOrserList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        orders = Order.objects.filter(user=self.kwargs['pk'])
        return orders