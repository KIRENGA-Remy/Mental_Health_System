from django.urls import path
from app import views

urlpatterns = [
    path('registeruser/', views.registeruser, name='registeruser'),
    path('alreadyexist', views.alreadyexist, name='alreadyexist'),
    path('login/', views.login, name='login'),
    path('', views.loginuser, name='loginuser'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_details/', views.patient_details, name='patient_details'),
    path('patients/', views.manage_patients, name='manage_patients'),
    path('availability/', views.set_availability, name='set_availability'),
    path('analytics/', views.analytics, name='analytics'),
    path('details_appointment/', views.details_appointment, name='details_appointment'),
    path('confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctors/', views.search_doctors, name='search_doctors'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/request-appointment/', views.request_appointment, name='request_appointment'),
    path('approved_appointments/', views.approved_appointments, name='approved_appointments'),
    # path('appointment/<int:patient_id>/', views.details_appointment, name='details_appointment'),
]