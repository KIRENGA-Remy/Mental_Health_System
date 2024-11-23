from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Appointment, DoctorModel, PatientModel

# Get the User model
User = get_user_model()

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Enter your first name"
    )
    last_name = forms.CharField(
        max_length=30, required=True, help_text="Enter your last name"
    )
    email = forms.EmailField(
        required=True, help_text="Enter your email"
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, required=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        """
        Ensure the email is unique.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email


# Custom Authentication Form
class CustomAuthenticationForm(forms.Form):
    error_messages = {
        "invalid_login": _("Please enter a correct email and password."),
        "inactive": _("This account is inactive."),
    }
    username = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email",
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
        }),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Override clean to authenticate using email and password.
        """
        email = self.cleaned_data.get("username")  # The field 'username' is mapped to email.
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Ensure the user is active and allowed to log in.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        """
        Return the authenticated user.
        """
        return self.user_cache

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user with email and password.
        """
        UserModel = get_user_model()  
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date']

class AppointmentRequestForm(forms.Form):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe your symptoms...'}),
        required=True
    )

class DoctorSearchForm(forms.Form):
    specialization = forms.ChoiceField(choices=[
        ('', 'Select specialization'),
        ('eyes', 'Eyes Specialist'),
        ('headache', 'Headache Specialist'),
        ('injury', 'Injury Specialist'),
    ])

class PatientSearchForm(forms.Form):
    SYMPTOM_CHOICES = [
        ('', 'Select Symptom'),
        ('eyes', 'Eye pain or discomfort'),
        ('headache', 'Persistent or severe headaches'),
        ('injury', 'Joint or muscle pain'),
    ]
    symptom = forms.ChoiceField(
        choices=SYMPTOM_CHOICES,
        required=True,
        label='Search by Symptom',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DoctorModel
        fields = ['specialization', 'bio', 'contact_number', 'available', 'location', 'working_hours']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe yourself'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'working_hours': forms.TextInput(attrs={'placeholder': 'e.g., Mon-Fri, 9AM-5PM'}),
        }

class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PatientModel
        fields = ['age', 'gender', 'symptoms', 'insurance']
        
        widgets = {
            'age': forms.NumberInput(attrs={'placeholder': 'Enter your age'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'symptoms': forms.Select(attrs={'class': 'form-select'}),
            'insurance': forms.Select(attrs={'class': 'form-select'}),
        }