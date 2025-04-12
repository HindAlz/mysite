
# Create your views here.
from django.shortcuts import render, redirect
from .forms import PatientSignupForm, StaffSignupForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.save()
            login(request, user)
            return redirect('patient_dashboard')  # Replace with an actual URL in your app
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
                return redirect('patient_dashboard')  # make sure this view/URL exists
            elif user.is_staff_member:
                return redirect('staff_dashboard')  # make sure this view/URL exists
            else:
                messages.error(request, "User type is not defined.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # This should match your login URL name

from django.http import HttpResponse

def patient_dashboard(request):
    return HttpResponse("Welcome, patient!")

def staff_dashboard(request):
    return HttpResponse("Welcome, staff!")
