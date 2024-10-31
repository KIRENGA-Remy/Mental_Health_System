from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Userdata, Doctor, Appointment, PatientProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate with email as username
        user = authenticate(request, username=email, password=password)  

        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')

    return render(request, 'login.html')


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


def patient_dashboard(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'patient_dashboard.html', {'doctors': doctors})


def request_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    patient_profile = request.user.patientprofile
    appointment = Appointment.objects.create(patient=patient_profile, doctor=doctor)
    return redirect('patient_dashboard')


def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor__user=request.user, status='Pending')
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})


def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.status = 'Confirmed'
        appointment.save()
        return redirect('doctor_dashboard')
    return render(request, 'confirm_appointment.html', {'appointment': appointment})


# Home page view after login
@login_required
def home(request):
    return render(request, 'home.html')

# View to display list of doctors
@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()  # Assuming a Doctor model exists with relevant fields
    return render(request, 'doctor_list.html', {'doctors': doctors})

# View to display approved appointments for the logged-in patient
@login_required
def approved_appointments(request):
    # Fetch approved appointments for the currently logged-in patient
    appointments = Appointment.objects.filter(patient=request.user, status='approved')
    return render(request, 'approved_appointments.html', {'appointments': appointments})


login_required
def doctor_list(request):
    doctors = Doctor.objects.all()  # Assuming a Doctor model exists
    return render(request, 'doctor_list.html', {'doctors': doctors})

# View to display specific doctor details
@login_required
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

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


@login_required
def approved_appointments(request):
    # Retrieve all approved appointments for the logged-in patient
    appointments = Appointment.objects.filter(patient=request.user, status='approved')
    return render(request, 'approved_appointments.html', {'appointments': appointments})


def patient_details(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        symptoms = request.POST.get('symptoms')

        # Save the data to the database (ensure you have a PatientProfile model)
        PatientProfile.objects.create(
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            age=age,
            symptoms=symptoms
        )
        
        return redirect('some_page_after_saving')  # Redirect to a confirmation or profile page

    return render(request, 'patient_details.html')