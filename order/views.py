from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from django.utils import timezone


def create_order(request):
    if request.method == 'GET':
        context = {'form': OrderForm()}
        return render(request, 'order/create_order.html', context)
    else:
        try:
            form = OrderForm(request.POST)
            new_order = form.save()
            new_order.save()
            return redirect('orders_list')
        except ValueError:
            context = {'form': OrderForm(), 'error': 'Bad Data'}
            return render(request, 'order/create_order.html', context)


def orders_list(request):
    orders = Order.get_all()
    return render(request, 'order/orders_list.html', {'orders': orders, 'is_all': True})


def not_returned(request):
    orders = Order.get_not_returned_books()
    return render(request, 'order/orders_list.html', {'orders': orders, 'is_all': False})


def delete_order(request, order_id):
    Order.delete_by_id(order_id)
    return redirect('orders_list')


def edit_order(request, order_id):
    order = Order.get_by_id(order_id)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        context = {'form': form}
        return render(request, 'order/edit_order.html', context)
    else:
        form = OrderForm(request.POST, instance=order)
        form.save()
        return redirect('orders_list')


def return_book(request, order_id):
    order = Order.get_by_id(order_id)
    order.end_at = timezone.now()
    order.save()
    return redirect('orders_list')
