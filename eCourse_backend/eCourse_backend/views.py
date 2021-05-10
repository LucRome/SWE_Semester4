from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect
from users.models import User

# the view for the homepage


@login_required
def homepage(request):
    type = request.user.type

    if type == 1 or request.user.is_superuser:
        return redirect('course_overview', page=1)
    elif type == 2:
        return redirect('course_overview', page=1)
    elif type == 3:
        return redirect('course_overview', page=1)
    else:
        return render(request, 'home/home_auth.html')
