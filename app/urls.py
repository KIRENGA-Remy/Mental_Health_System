from django.urls import path
from app import views

urlpatterns = [
    path('registeruser/', views.registeruser, name='registeruser'),
    path('already_exist/', lambda request: render(request, 'already_exist.html'), name='already_exist'),
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_details/', views.patient_details, name='patient_details'),
    path('details_appointment/', views.details_appointment, name='details_appointment'),
    path('confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/request-appointment/', views.request_appointment, name='request_appointment'),
    path('approved_appointments/', views.approved_appointments, name='approved_appointments'),
    # path('appointment/<int:patient_id>/', views.details_appointment, name='details_appointment'),
]