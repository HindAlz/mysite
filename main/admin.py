from django.contrib import admin
from .models import Patient, Staff, Appointment, VirtualAppointment, Bill, Resource, EmergencyEvent

admin.site.register(Patient)
admin.site.register(Staff)
admin.site.register(Appointment)
admin.site.register(VirtualAppointment)
admin.site.register(Bill)
admin.site.register(Resource)
admin.site.register(EmergencyEvent)
