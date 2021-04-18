from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import FileForm
from .models import Submission
import magic
import os

# Create your views here.
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

