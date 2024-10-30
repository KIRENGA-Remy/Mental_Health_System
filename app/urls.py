from django.urls import path
from app import views

urlpatterns = [
    path('', views.login, name='login'),
    # path(r'register/', views.register, name='register'),
    path('registeruser/', views.registeruser, name='registeruser'),
    # path('', views.home, name='home'),
]