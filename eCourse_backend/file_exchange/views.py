from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth.decorators import login_required
from .forms import FileForm
from .models import Submission

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
    fn = file.file.path
    response = FileResponse(open(fn, 'rb'))
    return response
