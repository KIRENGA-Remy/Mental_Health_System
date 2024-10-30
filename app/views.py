from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser, Userdata

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate with email as username
        user = authenticate(request, username=email, password=password)  # Note: username=email

        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')

    return render(request, 'login.html')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists.')
#             return render(request, 'register.html')

#         user = CustomUser.objects.create_user(username=username, email=email, password=password)
#         user.role = role
#         user.save()
#         messages.success(request, 'Registration successful.')
#         return redirect('login')

#     return render(request, 'register.html')


def registeruser(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname') 
        lastname = request.POST.get('lastname') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        print(f"Firstname: {firstname}, Lastname: {lastname} , Email: {email}, Password: {password}")

        
        if Userdata.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')
        
        # Save the user data
        query = Userdata( firstname=firstname,lastname=lastname, email=email, password=password)
        query.save()
        
        # Display success message
        messages.success(request, 'Registration successful.')
        return redirect('login')  

    return render(request, 'register.html')



def home(request):
    return render(request, 'home.html')