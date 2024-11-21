from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AppointmentForm
from django.contrib import messages
from .models import CustomUser, Appointment, HealthRecord, PatientRecord, Doctor, Patient

def registeruser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email):
                messages.error(request, "Account with this email already exist")
                return render(request, 'register.html', {'form':form})
            
            user = form.save(commit=False)
            if user.role == 'patient':
                user.save()
                Patient.objects.create(user=user)
            elif user.role == 'doctor':
                user.save()
                Doctor.objects.create(user=user)
        
        messages.success(request, "Account created successfully")
        return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form':form})


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
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    pending_appointments = appointments.filter(status='Pending')
    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'pending_appointments': pending_appointments,
    })


@login_required
def manage_patients(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    records = PatientRecord.objects.filter(doctor=doctor)
    return render(request, 'manage_patients.html', {'records': records})

@login_required
def set_availability(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    if request.method == 'POST':
        doctor.working_hours = request.POST.get('working_hours')
        doctor.available = request.POST.get('available', 'off') == 'on'
        doctor.save()
        return render(request, 'set_availability.html', {'success': True, 'doctor': doctor})
    return render(request, 'set_availability.html', {'doctor': doctor})

@login_required
def analytics(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)
    total_appointments = appointments.count()
    patient_visits = appointments.values('patient').distinct().count()
    return render(request, 'analytics.html', {
        'total_appointments': total_appointments,
        'patient_visits': patient_visits,
    })

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
    if request.user.is_authenticated and request.user.role == 'patient':
        patient = get_object_or_404(Patient, user=request.user)
        appointments = Appointment.objects.filter(patient=patient)
        health_records = HealthRecord.objects.filter(patient=patient)
        
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
