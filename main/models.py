from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)
    medical_history = models.TextField()
    insurance_info = models.TextField()

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    is_manager = models.BooleanField(default=False)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=20)

class VirtualAppointment(Appointment):
    link = models.URLField()
    is_active = models.BooleanField(default=False)

class Bill(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    insurance_covered = models.DecimalField(max_digits=10, decimal_places=2)

class Resource(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    expiry_date = models.DateField()
    location = models.CharField(max_length=100)
    managed_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

class EmergencyEvent(models.Model):
    location = models.CharField(max_length=200)
    triggered_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
