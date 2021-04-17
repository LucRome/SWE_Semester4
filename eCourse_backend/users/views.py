from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.forms.models import model_to_dict
from eCourse_backend.models import *
from .forms import *
from .models import User, Lecturer, Student
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

# Views given from Backend, use as orientation


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
        user_form = UserForm(request.POST)
        type_form = UsertypeChooseForm(request.POST)
        if type_form.is_valid() and user_form.is_valid():
            u_type = type_form.cleaned_data['user_type']
            if u_type == 'student':
                form = StudentForm(request.POST)
                form.save()
            elif u_type == 'lecturer':
                form = LecturerForm(request.POST)
                form.save()
            elif u_type == 'office':
                form = OfficeUserForm(request.POST)
                form.save()
    else:
        user_form = UserForm()
        type_form = UsertypeChooseForm()

    context = {
        'form': user_form,
        'usertype_form': type_form,
    }
    return render(request, 'users/create_user.html', context)


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
        'name': name,
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

    return render(request, 'users/alter_user.html', {'form': form})


# Views for the admin
# TODO: check whethter user is from the right group

# User administration

@login_required
@permission_required('users.manage_users', raise_exception=True)
def user_administration_admin(request):
    if request.method == 'GET':
        return render(request, 'admin/users/administration.html', {})

# IFrames
# create lecturer


@xframe_options_exempt  # can be solved better
@login_required
@permission_required('users.manage_users', raise_exception=True)
def create_lecturer_iframe(request):
    save_success = False
    if request.method == 'POST':
        user_form = LecturerForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            save_success = True
    else:
        user_form = LecturerForm()

    context = {
        'user_form': user_form,
        'success': save_success,
    }

    return render(request, 'admin/users/iframes/create_user/create_lecturer.html', context)


# create officeuser


@xframe_options_exempt  # can be solved better
@login_required
@permission_required('users.manage_users', raise_exception=True)
def create_officeuser_iframe(request):
    save_success = False
    if request.method == 'POST':
        user_form = OfficeUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            save_success = True
    else:
        user_form = OfficeUserForm()

    context = {
        'user_form': user_form,
        'success': save_success,
    }

    return render(request, 'admin/users/iframes/create_user/create_officeuser.html', context)


# create student


@xframe_options_exempt  # can be solved better
@login_required
@permission_required('users.manage_users', raise_exception=True)
def create_student_iframe(request):
    save_success = False
    if request.method == 'POST':
        user_form = StudentForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            save_success = True
    else:
        user_form = StudentForm()

    context = {
        'user_form': user_form,
        'success': save_success,
    }

    return render(request, 'admin/users/iframes/create_user/create_student.html', context)

# Student list


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def student_list_iframe(request, page=1):
    # TODO: filter + split into multiple pages
    students = Student.objects.all()
    return render(request, 'admin/users/iframes/student_list.html', {'students': students})


# Lecturer list

@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def lecturer_list_iframe(request, page=1):
    # TODO: filter + split into multiple pages
    lecturers = Lecturer.objects.all()
    return render(request, 'admin/users/iframes/lecturer_list.html', {'lecturers': lecturers})
