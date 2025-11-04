from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Student
from django.contrib.auth.decorators import login_required
from .forms import PreTestForm
def signup_view(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        student_id = request.POST['student_id']
        section = request.POST['section']
        age = request.POST['age']
        email = request.POST['email']
        password = request.POST['password']

        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "Student ID already exists.")
            return redirect('signup')

        student = Student.objects.create_user(
            student_id=student_id,
            fullname=fullname,
            section=section,
            age=age,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        student_id = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, student_id=student_id, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('pretest_form')  # change later to dashboard or form
        else:
            messages.error(request, "Invalid Student ID or Password.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def pretest_form(request):
    if request.method == 'POST':
        form = PreTestForm(request.POST)
        if form.is_valid():
            pretest = form.save(commit=False)
            pretest.student = request.user
            pretest.save()
            return redirect('student_dashboard')
    else:
        form = PreTestForm()

    return render(request, 'accounts/pretest_form.html', {'form': form})
