"""Idea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from idear import views as views
from idear import creations
from idear import projects
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'index$', views.index),
    url(r'login$', views.login),
    url(r'regist$', views.regist),
    url(r'team$', views.team),
    url(r'teamdetails$', views.teamdetails),
    url(r'creations$', creations.creations),
    url(r'forgetPassword$', views.forgetPassword),
    url(r'apply$', views.apply),
    url(r'recruit$', views.projects),
    url(r'redetails$', views.redetails),
    url(r'projects$', projects.projects),
    # url(r'test$', creations.Get_creation),
    # url(r'test$', creations.Get_creation)
    # url(r'test$', creations.Get_creation),
    # url(r'test$', creations.Get_creation)
    # url(r'projects$', projects.projects),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

