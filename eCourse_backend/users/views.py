from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from eCourse_backend.models import *
from .forms import *
from .models import User, Lecturer, Student, Office
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator

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
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserForm()

    context = {
        'form': user_form,
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
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            Lecturer.objects.create_user(
                username=user_form['username'].data,
                email=user_form['email'].data,
                first_name=user_form['first_name'].data,
                last_name=user_form['last_name'].data,
                matr_nr=user_form['matr_nr'].data
            )
            save_success = True
    else:
        user_form = UserForm()
    context = {
        'user_form': user_form,
        'success': save_success,
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
    if request.method == 'POST':
        user_form = StaffForm(request.POST)
        if user_form.is_valid():
            if user_form['is_superuser'].data:
                Office.objects.create_superuser(
                    username=user_form['username'].data,
                    email=user_form['email'].data,
                    first_name=user_form['first_name'].data,
                    last_name=user_form['last_name'].data,
                )
            else:
                Office.objects.create_user(
                    username=user_form['username'].data,
                    email=user_form['email'].data,
                    first_name=user_form['first_name'].data,
                    last_name=user_form['last_name'].data,
                )
            save_success = True
    else:
        user_form = StaffForm()
    context = {
        'user_form': user_form,
        'success': save_success,
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
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            Student.objects.create_user(
                username=user_form['username'].data,
                email=user_form['email'].data,
                first_name=user_form['first_name'].data,
                last_name=user_form['last_name'].data,
                matr_nr=user_form['matr_nr'].data
            )
            save_success = True
    else:
        user_form = UserForm()
    context = {
        'user_form': user_form,
        'success': save_success,
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
                matr_nr__contains=filter_form['matr_nr'].data,
                first_name__contains=filter_form['first_name'].data,
                last_name__contains=filter_form['last_name'].data,
                username__contains=filter_form['username'].data)
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
        filter_form = LecturerFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            lecturers = Lecturer.objects.filter(
                first_name__contains=filter_form['first_name'].data,
                last_name__contains=filter_form['last_name'].data,
                username__contains=filter_form['username'].data)
    else:
        filter_form = LecturerFilterForm()
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
        filter_form = AdminStaffFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            users = Office.objects.filter(
                first_name__contains=filter_form['first_name'].data,
                last_name__contains=filter_form['last_name'].data,
                username__contains=filter_form['username'].data)
    else:
        filter_form = AdminStaffFilterForm()
        users = Office.objects.all()

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'admin/users/iframes/staff_admin_list.html', context)

# Edit User IFrame

# TODO: correctly edit user


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def edit_user_admin_modalcontent_iframe(request, username):
    user_object = get_object_or_404(User, username=username)
    update_success = False
    if request.method == 'POST':
        form = StaffForm(request.POST or None, instance=user_object)
        if form.is_valid():
            form.save()
            update_success = True
    else:
        user_object = get_object_or_404(User, username=username)
        form = UserForm(data=model_to_dict(user_object))

    context = {
        'username': username,
        'user_form': form,
        'update_success': update_success
    }

    return render(request, 'admin/users/iframes/edit_user_modalcontent.html', context)


# Delete user Iframe

@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def delete_user_iframe(request, username):
    user_to_delete = get_object_or_404(User, username=username)
    # TODO: catch if delete operation fails (?)
    user_to_delete.delete()
    context = {
        'username': username,
    }
    return render(request, 'admin/users/iframes/deleted_user_iframe.html', context)
