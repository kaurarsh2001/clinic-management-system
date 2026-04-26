from django.contrib import admin
from django.urls import path
from core.views import home, doctor_dashboard, appointment_list, reports, patient_history
from core.views import login_view, logout_view
from core.views import export_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('appointments/', appointment_list, name='appointments'),
    path('reports/', reports, name='reports'),
    path('patient-history/<int:patient_id>/', patient_history, name='patient_history'),
    path('export-report/', export_report, name='export_report'),
]
