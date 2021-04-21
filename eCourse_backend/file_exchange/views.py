from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import FileForm, ExersiceForm
from .models import Submission
from courses.models import Exercise
import magic
import os

# Create your views here.

# exercise

@login_required
def overview(request):
    if request.method == 'GET':
        exercises = Exercise.objects.all()
        return render(request, 'file_exchange/overview.html', {'exersices': exercises})


@login_required
@permission_required('file_exchange.create_exercise', raise_exception=True)
def create_exercise(request):
    if request.method == 'POST':
        form = ExersiceForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ExersiceForm()

    return render(request, 'file_exchange/create_exersice.html', {'form': form})


@login_required
@permission_required('file_exchange.create_exercise', raise_exception=True)
def delete_exercise(request, id):
    exercise_to_delete = get_object_or_404(Exercise, pk=id)
    name = exercise_to_delete.name
    exercise_to_delete.delete()
    return render(request, 'file_exchange/deleted_exersice.html', {'name': name})

@login_required
@permission_required('file_exchange.create_exercise', raise_exception=True)
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
            # file is saved
            form.save()
            return render(request, 'file_exchange/sucess.html')
    else:
        form = FileForm()
    return render(request, 'file_exchange/upload_file.html', {'form': form})

@login_required
def download_file(request, id):
    file = get_object_or_404(Submission, pk=id)
    file_buffer = open(file.file.path, 'rb').read()
    content_type = magic.from_buffer(file_buffer, mime=True)
    response = HttpResponse(file_buffer, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="%s' %os.path.basename(file.file.path)
    return response

