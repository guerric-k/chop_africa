from django import forms

class ReservationFilterForm(forms.Form):
    date = forms.DateField(required=False)
    username = forms.CharField(max_length=150, required=False)
    table_number = forms.IntegerField(required=False)
