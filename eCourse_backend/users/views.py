from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.forms.models import model_to_dict
from eCourse_backend.models import *
from .forms import UserForm
from .models import User

# Create your views here.

@login_required
@permission_required('users.manage_users')
def overview(request):
    # TODO: Filter Users based on attributes (group, course, etc)
    if request.method == 'GET':
        all_users = User.objects.all()
        return render(request, 'users/overview.html', {'users': all_users})

@login_required
@permission_required('users.manage_users', raise_exception=True)
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()

    return render(request, 'users/create_user.html', {'form': form})

@login_required
@permission_required('users.manage_users', raise_exception=True)
def delete_user(request, id):
    user_to_delete = get_object_or_404(User, pk=id)
    # TODO: lecturers do not have matr_nr
    matr_nr = user_to_delete.matr_nr
    name = '{} {}'.format(user_to_delete.first_name, user_to_delete.last_name)
    user_to_delete.delete()
    context = {
        'matr_nr': matr_nr,
        'name' : name,
    }
    return render(request, 'users/deleted_user.html', context) 

@login_required
@permission_required('users.manage_users', raise_exception=True)
def alter_user(request, id):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        user_object = get_object_or_404(User, pk=id)
        form = UserForm(model_to_dict(user_object))

    return render(request, 'users/alter_user.html', {'form': form })
