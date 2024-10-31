from django.urls import path
from app import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('registeruser/', views.registeruser, name='registeruser'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('appointments/', views.approved_appointments, name='approved_appointments'),
]