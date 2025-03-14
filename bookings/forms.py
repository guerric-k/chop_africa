from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Table, Reservation, User  # Import your models

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
