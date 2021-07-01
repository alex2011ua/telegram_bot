from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserCreationForm



def create_user(request):
    if request.method == 'GET':
        context = {'form': UserCreationForm()}
        return render(request, 'authentication/create_user.html', context)
    else:
        try:
            form = UserCreationForm(request.POST)
            new_user = form.save()
            new_user.save()
            return redirect('users_list')
        except ValueError:
            context = {'form': UserCreationForm(), 'error': 'Bad Data'}
            return render(request, 'authentication/create_user.html', context)


def users_list(request):
    users = CustomUser.get_all()
    return render(request, 'authentication/users_list.html', {'users': users})


def delete_user(request, user_id):
    CustomUser.delete_by_id(user_id)
    return redirect('users_list')


def edit_user(request, user_id):
    user = CustomUser.get_by_id(user_id)
    if request.method == 'GET':
        form = UserCreationForm(instance=user)
        context = {'form': form}
        return render(request, 'authentication/edit_user.html', context)
    else:
        try:
            form = UserCreationForm(request.POST, instance=user)
            form.save()
            return redirect('users_list')
        except ValueError:
            context = {'form': UserCreationForm(), 'error': 'Bad Data'}
            return render(request, 'authentication/create_user.html', context)






