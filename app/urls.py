from django.urls import path
from app import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path(r'register/', views.register, name='register')
]