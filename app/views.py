from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Userdata, Doctor, Appointment, Patient
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages


# def registeruser(request):
#     if request.method == 'POST':
#         firstname = request.POST.get('firstname') 
#         lastname = request.POST.get('lastname') 
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
        
#         print(f"Firstname: {firstname}, Lastname: {lastname} , Email: {email}, Password: {password}")

        
#         if Userdata.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists.')
#             return render(request, 'register.html')
        
#         # Save the user data
#         query = Userdata( firstname=firstname,lastname=lastname, email=email, password=password)
#         query.save()
        
#         # Display success message
#         messages.success(request, 'Registration successful.')
#         return redirect('login')  

#     return render(request, 'register.html')


# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         # Authenticate with email as username
#         user = authenticate(request, username=email, password=password)  

#         if user:
#             auth_login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid email or password')
#             return render(request, 'login.html')

#     return render(request, 'login.html')


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def registeruser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else: 
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm()(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'doctor':
               return redirect('/doctor_dashboard')
            elif user.role == 'patient':
                return redirect('/patient_dashboard')
    else: 
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def doctor_dashboard(request):
    patients = Patient.objects.all()  # Get all patient profiles
    return render(request, 'doctor_dashboard.html', {'patients': patients})


# def patient_details(request):
#     if request.method == 'POST':
#         firstname = request.POST.get('firstname')
#         lastname = request.POST.get('lastname')
#         gender = request.POST.get('gender')
#         age = request.POST.get('age')
#         symptoms = request.POST.get('symptoms')

#         # Save the data to the database (ensure you have a Patient model)
#         Patient.objects.create(
#             firstname=firstname,
#             lastname=lastname,
#             gender=gender,
#             age=age,
#             symptoms=symptoms
#         )
        
#         return redirect('some_page_after_saving')  # Redirect to a confirmation or profile page

#     return render(request, 'patient_details.html')



@login_required
def patient_details(request):
    # Check if the logged-in user already has a profile
    try:
        patient_profile = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient_profile = None
    
    if request.method == 'POST':
        # Retrieve form data from POST request
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        symptoms = request.POST.get('symptoms')

        # If patient profile exists, update it; otherwise, create a new one
        if patient_profile:
            patient_profile.firstname = firstname
            patient_profile.lastname = lastname
            patient_profile.gender = gender
            patient_profile.age = age
            patient_profile.symptoms = symptoms
            patient_profile.save()
            messages.success(request, 'Your profile has been updated successfully.')
        else:
            Patient.objects.create(
                user=request.user,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                age=age,
                symptoms=symptoms
            )
            messages.success(request, 'Your profile has been created successfully.')
        
        # Redirect to the same page after saving
        return redirect('patient_details')

    # If a GET request, render the form with the existing profile data, if any
    return render(request, 'patient_details.html', {'patient_profile': patient_profile})

#h
def details_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        
        # Create appointment record for the patient
        Appointment.objects.create(
            patient=patient,
            doctor=request.user,  # Assuming the doctor is the logged-in user
            date=date,
            time=time,
            location=location
        )
        
        return redirect('doctor_dashboard')  # Redirect to the dashboard after saving
    
    return render(request, 'details_appointment.html', {'patient': patient})


def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.status = 'Confirmed'
        appointment.save()
        return redirect('doctor_dashboard')
    return render(request, 'confirm_appointment.html', {'appointment': appointment})

# _______________________________________________________
def patient_dashboard(request):
    doctors = Doctor.objects.all()
    return render(request, 'patient_dashboard.html', {'doctors': doctors})


# View to display specific doctor details
@login_required
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})


# def request_appointment(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     patient_profile = request.user.Patient
#     appointment = Appointment.objects.create(patient=patient_profile, doctor=doctor)
#     return redirect('patient_dashboard')



# View to handle appointment request
@login_required
def request_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Create an appointment request (adjust model fields as needed)
    appointment = Appointment.objects.create(
        patient=request.user,
        doctor=doctor,
        status='pending'  # Set the initial status as 'pending'
    )

    # Redirect to the appointment confirmation page
    messages.success(request, f"Your request for an appointment with Dr. {doctor.name} has been sent.")
    return render(request, 'request_appointment.html', {'doctor': doctor})


# View to display approved appointments for the logged-in patient
@login_required
def approved_appointments(request):
    # Fetch approved appointments for the currently logged-in patient
    appointments = Appointment.objects.filter(patient=request.user, status='approved')
    return render(request, 'approved_appointments.html', {'appointments': appointments})


def home(request):
    return render(request, 'home.html')


# Home page view after login
# @login_required
# def home(request):
#     return render(request, 'home.html')

# View to display list of doctors
# @login_required
# def doctor_list(request):
#     doctors = Doctor.objects.all()  # Assuming a Doctor model exists with relevant fields
#     return render(request, 'doctor_list.html', {'doctors': doctors})


login_required
def doctor_list(request):
    doctors = Doctor.objects.all()  # Assuming a Doctor model exists
    return render(request, 'doctor_list.html', {'doctors': doctors})
