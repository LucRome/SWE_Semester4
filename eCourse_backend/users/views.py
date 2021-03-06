from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from eCourse_backend.models import *
from .forms import *
from .models import User, Lecturer, Student, Office
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator
from eCourse_backend.utils import *

# Create your views here.

# Views given from Backend, use as orientation


# Views for the admin

# User administration

@login_required
@permission_required('users.manage_users', raise_exception=True)
def user_administration(request):
    if request.method == 'GET':
        return render(request, 'admin/users/administration.html', {})

# IFrames
# create lecturer


@xframe_options_exempt  # can be solved better
@login_required
@permission_required('users.manage_users', raise_exception=True)
def create_lecturer_iframe(request):
    user_pw = ''
    save_success = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            Lecturer.objects.create_user(
                username=get_value(user_form, 'username'),
                email=get_value(user_form, 'email'),
                first_name=get_value(user_form, 'first_name'),
                last_name=get_value(user_form, 'last_name'),
                password=get_value(user_form, 'password')
            )
            save_success = True
            user_pw = get_value(user_form, 'password')
    else:
        user_form = UserForm()
    context = {
        'user_form': user_form,
        'success': save_success,
        'user_pw': user_pw
    }

    return render(
        request,
        'admin/users/iframes/create_user/create_lecturer.html',
        context)


# create officeuser


@xframe_options_exempt  # can be solved better
@login_required
@permission_required('users.manage_users', raise_exception=True)
def create_officeuser_iframe(request):
    save_success = False
    user_pw = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            Office.objects.create_user(
                username=get_value(user_form, 'username'),
                email=get_value(user_form, 'email'),
                first_name=get_value(user_form, 'first_name'),
                last_name=get_value(user_form, 'last_name'),
                password=get_value(user_form, 'password')
            )
            save_success = True
            user_pw = get_value(user_form, 'password')
    else:
        user_form = UserForm()
    context = {
        'user_form': user_form,
        'success': save_success,
        'user_pw': user_pw
    }

    return render(
        request,
        'admin/users/iframes/create_user/create_officeuser.html',
        context)


# create student

@ xframe_options_exempt  # can be solved better
@ login_required
@ permission_required('users.manage_users', raise_exception=True)
def create_student_iframe(request):
    save_success = False
    user_pw = ''
    if request.method == 'POST':
        user_form = StudentForm(request.POST)
        if user_form.is_valid():
            Student.objects.create_user(
                username=get_value(user_form, 'username'),
                email=get_value(user_form, 'email'),
                first_name=get_value(user_form, 'first_name'),
                last_name=get_value(user_form, 'last_name'),
                matr_nr=get_value(user_form, 'matr_nr'),
                password=get_value(user_form, 'password')
            )
            save_success = True
            user_pw = get_value(user_form, 'password')
    else:
        user_form = StudentForm()
    context = {
        'user_form': user_form,
        'success': save_success,
        'user_pw': user_pw
    }

    return render(
        request,
        'admin/users/iframes/create_user/create_student.html',
        context)

# Student list


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def student_list_iframe(request, page=1):
    if request.method == 'POST':
        filter_form = StudentFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            students = Student.objects.filter(
                matr_nr__contains=get_value(filter_form, 'matr_nr'),
                first_name__contains=get_value(filter_form, 'first_name'),
                last_name__contains=get_value(filter_form, 'last_name'),
                username__contains=get_value(filter_form, 'username'),)
    else:
        filter_form = StudentFilterForm()
        students = Student.objects.all()

    paginator = Paginator(students, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'admin/users/iframes/student_list.html', context)


# Lecturer list

@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def lecturer_list_iframe(request, page=1):
    if request.method == 'POST':
        filter_form = LecturerAndOfficeFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            lecturers = Lecturer.objects.filter(
                first_name__contains=get_value(filter_form, 'first_name'),
                last_name__contains=get_value(filter_form, 'last_name'),
                username__contains=get_value(filter_form, 'username'),)
    else:
        filter_form = LecturerAndOfficeFilterForm()
        lecturers = Lecturer.objects.all()

    paginator = Paginator(lecturers, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'admin/users/iframes/lecturer_list.html', context)


# Staff and Admin List
@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def staff_admin_list_iframe(request, page=1):
    if request.method == 'POST':
        filter_form = LecturerAndOfficeFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            users = Office.objects.filter(
                first_name__contains=get_value(filter_form, 'first_name'),
                last_name__contains=get_value(filter_form, 'last_name'),
                username__contains=get_value(filter_form, 'username'),)
    else:
        filter_form = LecturerAndOfficeFilterForm()
        users = Office.objects.all()

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(
        request,
        'admin/users/iframes/staff_admin_list.html',
        context)

# Edit User IFrame

# TODO: correctly edit user


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def edit_user_admin_modalcontent_iframe(request, id):
    user_object = get_object_or_404(User, pk=id)
    update_success = False
    if request.method == 'POST':
        form = UserForm(request.POST or None, instance=user_object)
        if form.is_valid():
            form.save()
            update_success = True
    else:
        user_object = get_object_or_404(User, pk=id)
        form = UserForm(data=model_to_dict(user_object))

    context = {
        'id': id,
        'user_form': form,
        'update_success': update_success
    }

    return render(
        request,
        'admin/users/iframes/edit_user_modalcontent.html',
        context)

# Delete user Iframe


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def delete_user_iframe(request, id):
    user_to_delete = get_object_or_404(User, pk=id)
    # TODO: catch if delete operation fails (?)
    username = user_to_delete.username
    user_to_delete.delete()
    context = {
        'username': username,
    }
    return render(
        request,
        'admin/users/iframes/deleted_user_iframe.html',
        context)
