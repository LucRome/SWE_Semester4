from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required, login_required
from .forms import CourseForm, CourseStudentFilterForm
from users.models import User, Lecturer, Student, Office
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator
from .models import Course

# Create your views here.


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def course_student_list_iframe(request, name, page=1):
    # TO:DO Filter students by coursename

    if request.method == 'POST':
        filter_form = CourseStudentFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            students = Student.objects.filter(
                matr_nr__contains=filter_form['matr_nr'].data,
                first_name__contains=filter_form['first_name'].data,
                last_name__contains=filter_form['last_name'].data,
                username__contains=filter_form['username'].data)
    else:
        filter_form = CourseStudentFilterForm()
        students = Student.objects.all()

    paginator = Paginator(students, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'courses/iframes/course_student_list.html', context)


@login_required
@permission_required('courses.create_course', raise_exception=True)
def course_overview(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'courses/overview.html', {'courses': courses})


@login_required
@permission_required('courses.create_course', raise_exception=True)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # We need the students to add to this
            form.save()
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})


@login_required
@permission_required('courses.create_course', raise_exception=True)
def create_course_admin(request):
    success = False
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # We need the students to add to this
            form.save()
            success = True
    else:
        form = CourseForm()

    context = {
        'form': form,
        'success': success
    }
    return render(request, 'courses/create_course_admin.html', context)


@login_required
@permission_required('courses.alter_course', raise_exception=True)
def alter_course(request, id):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        course_object = get_object_or_404(Course, pk=id)
        form = CourseForm(model_to_dict(course_object))

    return render(request, 'courses/alter_course.html', {'form': form})


@login_required
@permission_required('courses.delete_course', raise_exception=True)
def delete_course(request, id):
    course_to_delete = get_object_or_404(Course, pk=id)
    name = course_to_delete.name
    course_to_delete.delete()

    return render(request, 'courses/deleted_course.html', {'name': name})


@login_required
@permission_required('courses.alter_course', raise_exception=True)
def edit_course(request, id):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        course_object = get_object_or_404(Course, pk=id)
        form = CourseForm(model_to_dict(course_object))

    return render(request, 'admin/edit_course.html', {'form': form})
