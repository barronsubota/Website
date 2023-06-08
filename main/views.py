# Create your views here.
# students/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from slugify import slugify
from django.utils import timezone
from .models import StudentCard
from datetime import datetime
import datetime

def home(request):
    today = datetime.date.today()
    year = today.strftime("%Y") 
    return render(request, 'pages/index.html', {'date': year})

@login_required
def remote_education(request):
    return render(request, 'students/remote_education_lobby.html', {})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        series = request.POST['series']
        issue_date = request.POST['issue_date']
        valid_until = request.POST['valid_until']
        surname = request.POST['surname']
        name = request.POST['name']
        patronymic = request.POST['patronymic']
        form_of_study = request.POST['form_of_study']
        faculty = request.POST['faculty']
        structural_unit = request.POST['structural_unit']
        group_number = request.POST['group_number']

        # Perform validation and matching with staff student ID data
        if series == 'staff_series' and valid_until >= timezone.now().date():
            slug = slugify(f'{name} {surname}')
            user = User.objects.create_user(username=username, password=password)
            student_card = StudentCard(
                user=user,
                series=series,
                issue_date=issue_date,
                valid_until=valid_until,
                surname=surname,
                name=name,
                patronymic=patronymic,
                form_of_study=form_of_study,
                faculty=faculty,
                structural_unit=structural_unit,
                group_number=group_number,
                slug=slug,
            )
            student_card.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid student ID data.')

    return render(request, 'students/register.html')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'students/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    student_card = StudentCard.objects.get(user=request.user)
    return render(request, 'students/profile.html', {'student_card': student_card})

def add_card(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        series = request.POST['series']
        issue_date = request.POST['issue_date']
        valid_until = request.POST['valid_until']
        surname = request.POST['surname']
        name = request.POST['name']
        patronymic = request.POST['patronymic']
        form_of_study = request.POST['form_of_study']
        faculty = request.POST['faculty']
        structural_unit = request.POST['structural_unit']
        group_number = request.POST['group_number']

        student_card = StudentCard(
            series=series,
            issue_date=issue_date,
            valid_until=valid_until,
            surname=surname,
            name=name,
            patronymic=patronymic,
            form_of_study=form_of_study,
            faculty=faculty,
            structural_unit=structural_unit,
            group_number=group_number
        )
        student_card.save()
        messages.success(request, 'Student card added successfully.')
        return redirect('add_card')

    return render(request, 'students/add_card.html')

