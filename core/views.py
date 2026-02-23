from django.shortcuts import render
from .models import Doctor, Patient, Appointment

def home(request):
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='Pending').count()

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
    }

    return render(request, 'core/home.html', context)
