
# Create your views here.
from django.shortcuts import render, redirect
from .forms import PatientSignupForm, StaffSignupForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from main.models import Appointment  # assumes Appointment is in your main app

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
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from main.models import Appointment  # or from .models if Appointment is in accounts

@login_required
def calendar_page(request):
    return render(request, 'accounts/staff_calendar.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from main.models import Appointment

@csrf_exempt
def update_appointment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        appt_id = data.get('id')
        new_title = data.get('title')

        try:
            appt = Appointment.objects.get(id=appt_id)
            appt.appointment_type = new_title
            appt.save()
            return JsonResponse({'success': True})
        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Appointment not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appt = Appointment.objects.get(id=data['id'])
            appt.appointment_type = data['title']
            appt.date = data['datetime']
            appt.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def delete_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appt = Appointment.objects.get(id=data['id'])
            appt.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


from django.http import JsonResponse
from main.models import Appointment
from datetime import timedelta


def calendar_data(request):
    # Fetch all appointments
    appointments = Appointment.objects.all()
    events = []

    for appt in appointments:
        events.append({
            "id": appt.id,  # Ensure the ID is included for edit/delete
            "title": f"{appt.patient.age} - {appt.appointment_type}",
            "start": appt.date.isoformat(),
            "end": (appt.date + timedelta(hours=1)).isoformat(),
        })

    return JsonResponse(events, safe=False)
