from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db.models import Count
from .models import Doctor, Patient, Appointment


# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})

    return render(request, 'core/login.html')


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')


# HOME DASHBOARD
@login_required
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


# DOCTOR DASHBOARD
@login_required
def doctor_dashboard(request):
    total_appointments = Appointment.objects.count()
    pending = Appointment.objects.filter(status='Pending').count()
    completed = Appointment.objects.filter(status='Completed').count()

    context = {
        'total_appointments': total_appointments,
        'pending': pending,
        'completed': completed,
    }

    return render(request, 'core/doctor_dashboard.html', context)


# APPOINTMENT LIST
@login_required
def appointment_list(request):
    query = request.GET.get('q')

    if query:
        appointments = Appointment.objects.filter(
            patient__user__username__icontains=query
        )
    else:
        appointments = Appointment.objects.all()

    context = {
        'appointments': appointments
    }

    return render(request, 'core/appointment_list.html', context)


# UPDATE APPOINTMENT STATUS
@login_required
def update_status(request, appointment_id, status):
    appointment = Appointment.objects.get(id=appointment_id)

    if status in ['Pending', 'Completed', 'Cancelled']:
        appointment.status = status
        appointment.save()

    return redirect('appointments')


# PATIENT HISTORY
@login_required
def patient_history(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'appointments': appointments
    }

    return render(request, 'core/patient_history.html', context)


# REPORTS PAGE
@login_required
def reports(request):

    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    pending = Appointment.objects.filter(status='Pending').count()
    completed = Appointment.objects.filter(status='Completed').count()

    doctor_reports = Appointment.objects.values(
        'doctor__user__username'
    ).annotate(total=Count('id'))

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending': pending,
        'completed': completed,
        'doctor_reports': doctor_reports
    }

    return render(request, 'core/reports.html', context)


# EXPORT REPORT TO PDF
@login_required
def export_report(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clinic_report.pdf"'

    p = canvas.Canvas(response)

    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    p.drawString(100, 800, "Clinic Management System Report")
    p.drawString(100, 760, f"Total Doctors: {total_doctors}")
    p.drawString(100, 740, f"Total Patients: {total_patients}")
    p.drawString(100, 720, f"Total Appointments: {total_appointments}")

    p.showPage()
    p.save()

    return response