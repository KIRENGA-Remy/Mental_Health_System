from django.urls import path
from app import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('registeruser/', views.registeruser, name='registeruser'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('appointments/', views.approved_appointments, name='approved_appointments'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/request-appointment/', views.request_appointment, name='request_appointment'),
    path('approved_appointments/', views.approved_appointments, name='approved_appointments'),
    path('patient_details/', views.patient_details, name='patient_details'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointment/<int:patient_id>/', views.details_appointment, name='details_appointment'),
]