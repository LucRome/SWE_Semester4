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
    # user administration
    path('admin/user_administration/',
         user_administration, name='user_administration'),
    # create user iframes
    path('admin/iframes/create_lecturer', create_lecturer_iframe,
         name='createlecturer_admin_iframe'),
    path('admin/iframes/create_officeuser', create_officeuser_iframe,
         name='createofficeuser_admin_iframe'),
    path('admin/iframes/create_student', create_student_iframe,
         name='createstudent_admin_iframe'),
    # deleted user iframe
    path('admin/iframes/deleted_user/<username>', delete_user_iframe,
         name='deleteuser_admin_iframe'),
    # edit user iframe
    path('admin/iframes/edit_student/<username>', edit_user_admin_modalcontent_iframe,
         name='edituser_admin_modalcontent_iframe'),
    # studentlist iframe
    path('admin/iframes/studentlist/page<int:page>',
         student_list_iframe, name='studentlist_admin_iframe'),
    # lecturerlist iframe
    path('admin/iframes/lecturerlist/page<int:page>',
         lecturer_list_iframe, name='lecturerlist_admin_iframe'),
    # admin + staff list (iframe)
    path('admin/iframes/adminstafflist/page<int:page>',
         staff_admin_list_iframe, name='adminlist_admin_iframe'),
]
