"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from . import views
from django.urls import path
from django.shortcuts import redirect
urlpatterns = [
    path('', lambda request: redirect('index/')),
    path('index/', views.index, name='index'),
    path('alllogin/', views.Alllogin, name='alllogin'),
    path('login/', views.Login, name='login'),  # 登录路由
    path('doctor-loginfirst/', views.Doctor_loginfirst, name='doctor-loginfirst'),
    path('doctor-page/', views.Doctor_page, name='doctor-page'),
    path('register/', views.Register, name='register'),  # 注册路由
    path('main-page/', views.Main_page, name='main-page'),
    path('main-page/account/', views.Account, name='account'),
    path('personalfile/', views.Personalfile, name='personalfile'),
    path('build-personalfile/', views.Build_personalfile, name='build-personalfile'),
    path('familyfile/', views.Familyfile, name='familyfile'),
    path('inquire/', views.Inquire, name='inquire'),
    path('online-register/', views.Online_register, name='online-register'),
    path('account/', views.Account, name='account'),
]


