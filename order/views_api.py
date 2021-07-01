from rest_framework import generics
from .serializers import OrderSerializer
from .models import Order


class OrderApiList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderApiCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer


class OrderApiDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
