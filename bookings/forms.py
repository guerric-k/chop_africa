from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Table, Reservation, User  # Imports the Table and Reservation models from the models.py file.

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'location']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'number_of_guests', 'status', 'special_requests', 'has_children', 'number_of_children', 'is_disabled', 'disability_details']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        has_children = cleaned_data.get('has_children')
        number_of_children = cleaned_data.get('number_of_children')
        is_disabled = cleaned_data.get('is_disabled')
        disability_details = cleaned_data.get('disability_details')

        if date and date < timezone.now().date():
            raise ValidationError("Reservation date cannot be in the past.")

        if has_children and number_of_children is None:
            raise ValidationError("Please specify the number of children.")

        if is_disabled and not disability_details:
            raise ValidationError("Please provide disability accommodation details.")

        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username', 'password_hash', 'has_children', 'number_of_children', 'is_disabled', 'disability_adjustments']
        widgets = {
            'password_hash': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password_hash')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password_hash = make_password(self.cleaned_data['password_hash'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)