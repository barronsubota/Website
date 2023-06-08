# students/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-card/', views.add_card, name='add_card'),
    path('profile/', views.profile, name='profile'),
    path('remote-education/', views.remote_education, name="remote"),
]
