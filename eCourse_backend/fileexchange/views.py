from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import FileForm, ExersiceForm
from .models import Submission
from courses.models import Exercise
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
# @permission_required('courses.add_exercise', raise_exception=True)
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
@permission_required('exercise.delete_exercise', raise_exception=True)
def delete_exercise(request, id):
    exercise_to_delete = get_object_or_404(Exercise, pk=id)
    name = exercise_to_delete.name
    exercise_to_delete.delete()
    return render(request,
                  'file_exchange/deleted_exersice.html',
                  {'name': name})


@login_required
@permission_required('exercise.change_exercise', raise_exception=True)
def alter_exersice(request, id):
    if request.method == 'POST':
        form = ExersiceForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        course_object = get_object_or_404(Exercise, pk=id)
        form = Exercise(model_to_dict(course_object))

    return render(request, 'file_exchange/alter_exercise.html', {'form': form})

# fileupload


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user_id = request.user.id
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
