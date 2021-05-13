from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, FileResponse, HttpResponse, request
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.db.models import Q
from .forms import FileForm, ExersiceForm
from .models import Submission
from courses.models import Exercise
from django.views.decorators.clickjacking import xframe_options_exempt
import re

# Create your views here.

# exercise


@login_required
def overview(request):
    if request.method == 'GET':
        exercises = Exercise.objects.all()
        return render(request,
                      'file_exchange/overview.html',
                      {'exersices': exercises})


@login_required
@permission_required('courses.add_exercise', raise_exception=True)
def create_exercise(request):
    save_success = False
    if request.method == 'POST':
        form = ExersiceForm(request.POST)
        if form.is_valid():
            form.save()
            save_success = True
    else:
        form = ExersiceForm()

    context = {
        'form': form,
        'save_success': save_success
    }

    return render(request,
                  'file_exchange/create_exersice.html',
                  context)


@login_required
@permission_required('courses.delete_exercise', raise_exception=True)
def delete_exercise(request, id):
    exercise_to_delete = get_object_or_404(Exercise, pk=id)
    id = exercise_to_delete.id
    exercise_to_delete.delete()

    if request.user.type == 1 or request.user.is_superuser:
        base_template = 'admin/home_admin.html'
    elif request.user.type == 2:
        base_template = 'lecturer/home_lecturer.html'

    context = {
        'base_template': base_template,
    }

    return render(request,
                  'file_exchange/deleted_exersice.html',
                  context)

# can be called by Lecturer and admin


@login_required
@permission_required('courses.change_exercise', raise_exception=True)
def alter_exersice(request, id):
    update_success = False
    if request.method == 'POST':
        exercise = get_object_or_404(Exercise, pk=id)
        form = ExersiceForm(request.POST or None, instance=exercise)
        if form.is_valid():
            form.save()
            update_success = True
    else:
        course_object = get_object_or_404(Exercise, pk=id)
        form = ExersiceForm(instance=course_object)

    if request.user.type == 1 or request.user.is_superuser:
        base_template = 'admin/home_admin.html'
    elif request.user.type == 2:
        base_template = 'lecturer/home_lecturer.html'

    context = {
        'base_template': base_template,
        'id': id,
        'form': form,
        'update_success': update_success
    }

    return render(request, 'file_exchange/alter_exercise.html', context)

    return render(request, 'file_exchange/alter_exercise.html', context)
# fileupload


@login_required
def upload_file(request, exercise_id):
    exercise_object = Exercise.objects.get(pk=exercise_id)
    if request.method == 'POST':
        # submission deadline does not matter for lecturer and office user
        if (request.user.type == 3 and timezone.now()
                > exercise_object.submission_deadline):
            # student is too late to upload redirect elsewhere
            return render(request, 'file_exchange/overview.html')
        else:
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.user_id = request.user.id
                submission.exercise_id = exercise_object.id
                if (request.user.type == 1 or request.user.type == 2):
                    submission.from_lecturer = True
                submission.save()
                # back to exercises overview
                return render(request, 'file_exchange/overview.html')
    else:
        form = FileForm()
    return render(request, 'file_exchange/upload_file.html', {'form': form})


@login_required
def download_file(request, id):
    file = get_object_or_404(Submission, pk=id)
    path = file.file.name
    f = open(path, 'rb').read()
    # type is static to pdf would cause an error if i try to downlaod a non
    # pdf file but we are only allowed to upload pdfs so its fine
    response = HttpResponse(f, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s' % filename(
        path)
    return response

# return filename w/o os.path.basename()


def filename(path):
    x = re.search("^upload/course_[0-9]+/exercise_[0-9]+/", path)
    path_path = x.group()
    filename = path.replace(path_path, '')
    return filename


@login_required
@xframe_options_exempt
def upload_site(request, id):
    exercise_object = Exercise.objects.get(pk=id)
    if request.method == 'POST':
        # submission deadline does not matter for lecturer and office user
        if (request.user.type == 3 and timezone.now()
                > exercise_object.submission_deadline):
            # student is too late to upload redirect elsewhere
            return render(request, 'file_exchange/iframes/upload_expired.html')
        else:
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.user_id = request.user.id
                submission.exercise_id = exercise_object.id
                if (request.user.type == 1 or request.user.type == 2):
                    submission.from_lecturer = True
                submission.save()
                return render(request, 'file_exchange/iframes/upload_site.html', {'form': form, })
    else:
        form = FileForm()
    return render(request, 'file_exchange/iframes/upload_site.html', {'form': form, })


@login_required
def exersice_site(request, id):
    files_lecturer = []
    files_student = []
    if (request.user.type == 1 or request.user.type == 2):
        file = Submission.objects.filter(exercise=id, from_lecturer=1)
        files_lecturer = help_files(file)
        file = Submission.objects.filter(exercise=id, from_lecturer=0)
        files_student = help_files(file)
    elif request.user.type == 3:
        file = (Submission.objects.filter(
                (Q(user=request.user.id)), exercise=id))
        files_student = help_files(file)
        file = (Submission.objects.filter(from_lecturer=1, exercise=id))
        files_lecturer = help_files(file)

    data = {'files_student': files_student,
            'files_lecturer': files_lecturer,
            'exersiceID': id}
    if request.user.type == 3:
        return render(request, 'file_exchange/student_exersice.html', data)
    elif (request.user.type == 1 or request.user.type == 2):
        return render(request, 'file_exchange/lecturer_exersice.html', data)
    else:
        return render(request, 'file_exchange/overview.html')


def help_files(file):
    res = []
    if file:
        for f in file:
            res.append(f)
    return res
