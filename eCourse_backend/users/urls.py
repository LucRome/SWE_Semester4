"""courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('overview/', overview, name='overview'),
    path('create/', create_user, name='create_user'),
    path('alter/<int:id>', alter_user, name='alter_user'),
    path('delete/<int:id>', delete_user, name='delete_user'),
    # user administration
    path('admin_s/user_administration/',
         user_administration_admin, name='user_administration_admin'),
    # create user iframes
    path('admin_s/iframes/create_lecturer', create_lecturer_iframe,
         name='createlecturer_admin_iframe'),
    path('admin_s/iframes/create_officeuser', create_officeuser_iframe,
         name='createofficeuser_admin_iframe'),
    path('admin_s/iframes/create_student', create_student_iframe,
         name='createstudent_admin_iframe'),
    # studentlist iframe
    path('admin_s/iframes/studentlist/page<int:page>',
         student_list_iframe, name='studentlist_admin_iframe'),
    # lecturerlist iframe
    path('admin_s/iframes/lecturerlist/page<int:page>',
         lecturer_list_iframe, name='lecturerlist_admin_iframe'),
    # admin + staff list (iframe)
    path('admin_s/iframes/adminstafflist/page<int:page>',
         staff_admin_list_iframe, name='adminlist_admin_iframe'),
]
