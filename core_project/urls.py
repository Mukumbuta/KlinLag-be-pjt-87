"""core_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('api/', include('klin_api.urls')),
    path('change_password', auth_views.PasswordChangeView.as_view(template_name= 'password/password_change.html'),
         name='password_change'),
    path('change_password/done', auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html'),
         name='password_change_done'),

    path('password_reset', auth_views.PasswordResetView.as_view(template_name= 'password/password_reset.html',
         subject_template_name='password/password_reset_subject.txt',
                                                                email_template_name='password/password_reset_email.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('activation_sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]


