from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Doctor, Appointment, Patient, CustomUser
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from django.contrib import messages
from django.contrib import messages
from .forms import CustomUserCreationForm, AppointmentForm
from .models import CustomUser, Appointment, HealthRecord

def registeruser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'register.html', {'form': form})  
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def alreadyexist(request):
    return render(request, 'alreadyexist.html')

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role == 'doctor':
                return redirect('/doctor_dashboard')
            elif user.role == 'patient':
                return redirect('/patient_dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def loginuser(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role == 'doctor':
                return redirect('/doctor_dashboard')
            elif user.role == 'patient':
                return redirect('/patient_dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def doctor_dashboard(request):
    patients = Patient.objects.all()  # Get all patient profiles
    return render(request, 'doctor_dashboard.html', {'patients': patients})

@login_required
def patient_details(request):
    try:
        patient_profile = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient_profile = None
    
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        symptoms = request.POST.get('symptoms')

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

        return redirect('patient_details')

    return render(request, 'patient_details.html', {'patient_profile': patient_profile})

def details_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')

        Appointment.objects.create(
            patient=patient,
            doctor=request.user, 
            date=date,
            time=time,
            location=location
        )
        
        return redirect('doctor_dashboard')  
    
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
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(patient=request.user)
        health_records = HealthRecord.objects.filter(patient=request.user)
        return render(request, 'patient_dashboard.html', {
            'appointments': appointments,
            'health_records': health_records
        })
    return redirect('login')


def search_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'search_doctors.html', {'doctors': doctors})


def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

@login_required
def request_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    appointment = Appointment.objects.create(
        patient=request.user,
        doctor=doctor,
        status='pending'  
    )

    messages.success(request, f"Your request for an appointment with Dr. {doctor.name} has been sent.")
    return render(request, 'request_appointment.html', {'doctor': doctor})

@login_required
def approved_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user, status='approved')
    return render(request, 'approved_appointments.html', {'appointments': appointments})


def home(request):
    return render(request, 'home.html')

login_required
def doctor_list(request):
    doctors = Doctor.objects.all()  
    return render(request, 'doctor_list.html', {'doctors': doctors})
