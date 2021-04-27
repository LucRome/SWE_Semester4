from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import permission_required, login_required
from .forms import CourseForm
from .models import Course, Exercise
from users.models import User
from file_exchange.models import Submission
from django.db.models import Q

# Create your views here.


@login_required
def course_overview(request):
    user_id = request.user.id
    if request.method == 'GET':
        # officer has type 3 in db
        if request.user.type == 3:
            courses = Course.objects.all()
        else:
            courses = Course.objects.filter(
                Q(student=user_id) | Q(lecturer_id=user_id))
        return render(request, 'courses/overview.html', {'courses': courses})


@login_required
def view_course(request, id):
    if request.method == 'GET':
        course = get_object_or_404(Course, pk=id)
        print('user type ', request.user.type)
        if (request.user.type == 3 or request.user.type == 2):
            # course members
            lecturer_id = course.lecturer_id
            lecturer = User.objects.get(id=lecturer_id)
            lecturer_name = lecturer.first_name + ' ' + lecturer.last_name
            students = list()
            for student in course.student.all():
                student_name = student.first_name + ' ' + student.last_name
                students.append(student_name)
        
            #exercises
            exercise = Exercise.objects.filter(course_id = id)

            #files
            files = dir()
            for e in exercise:
                print(e.id)
                files[e.id] = Submission.objects.filter(exercise = e.id)

            data = {'lecturer': lecturer_name, 'students': students, 'exercise' : exercise, 'files': files}

        #student
        if (request.user.type == 1):
            #exercises
            exercise = Exercise.objects.filter(course_id = id)
            print(exercise)

            files = dir()
            for e in exercise:
                files[e.id] = Submission.objects.filter((Q(user = request.user.id) | Q(from_lecturer = 1)), exercise = e.id)
            
            data = {'exercise' : exercise, 'files': files}

    return render(request, 'courses/detail.html', data)


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
