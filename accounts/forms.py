from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class PatientSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class StaffSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import PatientSignupForm, StaffSignupForm
from .models import CustomUser

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.save()
            login(request, user)
            return redirect('patient_dashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = PatientSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def staff_signup(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff_member = True
            user.save()
            login(request, user)
            return redirect('staff_dashboard')
    else:
        form = StaffSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_staff_member:
                return redirect('staff_dashboard')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
