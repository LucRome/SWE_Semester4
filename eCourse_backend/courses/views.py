from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required, login_required
from .forms import CourseForm, CourseStudentFilterForm
from users.models import User, Lecturer, Student, Office
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator
from .models import Course, Exercise
from users.models import User
from file_exchange.models import Submission
from django.db.models import Q

# Create your views here.


@xframe_options_exempt
@login_required
@permission_required('users.manage_users', raise_exception=True)
def course_student_list_iframe(request, id, page=1):
    # TO:DO Filter students by coursename

    if request.method == 'POST':
        filter_form = CourseStudentFilterForm(
            request.POST, )
        if filter_form.is_valid():
            # Filter
            students = Student.objects.filter(
                matr_nr__contains=get_value(filter_form, 'matr_nr'),
                first_name__contains=get_value(filter_form, 'first_name'),
                last_name__contains=get_value(filter_form, 'last_name'),
                username__contains=get_value(filter_form, 'username'))
    elif request.method == 'GET':
        filter_form = CourseStudentFilterForm()
        course = get_object_or_404(Course, pk=id)
        lecturer = course.lecturer
        students = course.student.all()

    context = {
        'filter_form': filter_form,
        'lecturer': lecturer,
        'students': students,
    }
    return render(request, 'courses/iframes/course_student_list.html', context)


@login_required
def course_overview(request, page=1):

    user_id = request.user.id
    if request.method == 'GET':
        # office user has type 1 in db
        if request.user.type == 1:
            courses = Course.objects.all()
        else:
            courses = Course.objects.filter(
                Q(student=user_id) | Q(lecturer_id=user_id))

    paginator = Paginator(courses, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'courses/overview.html', context)


@login_required
def view_course(request, id):
    if request.method == 'GET':
        course = get_object_or_404(Course, pk=id)
        print('user type ', request.user.type)
        # office user and lecturer
        if (request.user.type == 1 or request.user.type == 2):
            # course members
            lecturer_id = course.lecturer_id
            lecturer = User.objects.get(id=lecturer_id)
            lecturer_name = lecturer.first_name + ' ' + lecturer.last_name
            students = list()
            for student in course.student.all():
                student_name = student.first_name + ' ' + student.last_name
                students.append(student_name)

            # exercises
            exercise = Exercise.objects.filter(course_id=id)

            # files
            files = dir()
            for e in exercise:
                print(e.id)
                files[e.id] = Submission.objects.filter(exercise=e.id)

            data = {
                'lecturer': lecturer_name,
                'students': students,
                'exercise': exercise,
                'files': files}

        # student
        if (request.user.type == 3):
            # exercises
            exercise = Exercise.objects.filter(course_id=id)
            print(exercise)

            files = dir()
            for e in exercise:
                files[e.id] = Submission.objects.filter(
                    (Q(user=request.user.id) | Q(from_lecturer=1)), exercise=e.id)

            data = {'exercise': exercise, 'files': files}

    return render(request, 'courses/detail.html', data)


@login_required
@permission_required('courses.create_course', raise_exception=True)
def create_course(request):
    success = False
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # We need the students to add to this
            form.save()
            success = True
    else:
        form = CourseForm()

    if request.user.is_superuser or request.user.type == 1:
        base_template = 'admin/home_admin.html'
    elif request.user.type == 2:
        base_template = 'lecturer/home_lecturer.html'

    context = {
        'form': form,
        'success': success,
        'base_template': base_template
    }
    return render(request, 'courses/create_course.html', context)


@login_required
@permission_required('courses.delete_course', raise_exception=True)
def delete_course(request, id):
    # TODO: use for delete course
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

    return render(request, 'courses/edit_course.html',
                  {'form': form, 'courseid': id})
