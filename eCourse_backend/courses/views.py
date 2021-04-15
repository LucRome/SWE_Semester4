from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required, login_required
from .forms import CourseForm
from .models import Course

# Create your views here.


@login_required
@permission_required('courses.create_course', raise_exception=True)
def overview(request):
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
