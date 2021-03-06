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
    path('delete/<id>', delete_course, name='delte_course'),
    # course
    path('overview/page<int:page>', course_overview, name='course_overview'),
    # create course iframes
    path('iframes/detailed/<id>', detailed_course,
         name='detailed_course'),
    # admin: create course
    path('create/', create_course, name="create_course"),

    path('edit/<id>', edit_course, name='edit_course'),
]
