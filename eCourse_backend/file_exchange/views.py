from django.shortcuts import render
from django.http import HttpResponseRedirect
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