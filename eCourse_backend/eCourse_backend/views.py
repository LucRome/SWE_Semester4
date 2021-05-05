from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from users.models import User

# the view for the homepage


@login_required
def homepage(request):
    type = request.user.type

    if type == 1 or request.user.is_superuser:
        return render(request, 'admin/home_admin.html')
    elif type == 2:
        return render(request, 'lecturer/home_lecturer.html')
    elif type == 3:
        return render(request, 'student/home_student.html')
    else:
        return render(request, 'home/home_auth.html')
