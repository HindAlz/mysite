from django.urls import path
from . import views

urlpatterns = [
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('signup/staff/', views.staff_signup, name='staff_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
]
