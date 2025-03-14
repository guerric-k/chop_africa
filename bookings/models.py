from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.hashers import check_password, make_password

# Create your models here.

class Table(models.Model):
    """Model representing a restaurant table"""
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=50, choices=[
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('balcony', 'Balcony'),
        ('private', 'Private Room')
    ])
    
    class Meta:
        """Metadata options for the Table model."""
        ordering = ['number'] # Orders the table objects in ascending order.

    def __str__(self):
        return f"Table {self.number} ({self.capacity} people) - {self.get_location_display()}"
    
class Reservation(models.Model):
    """Model representing a table reservation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    has_children = models.BooleanField(default=False)
    number_of_children = models.IntegerField(null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    disability_details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'time']
        unique_together = ['table', 'date', 'time']  # Prevent double booking
    
    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"
    
    def clean(self):
        # Check if reservation date is in the past
        if self.date < timezone.now().date():
            raise ValidationError("Reservation date cannot be in the past.")
        
        # Check if a user already has a reservation on the same day
        same_day_reservations = Reservation.objects.filter(
            user=self.user, 
            date=self.date
        ).exclude(pk=self.pk)
        
        if same_day_reservations.exists():
            raise ValidationError("You already have a reservation for this day.")
        
        # Validate children information
        if self.has_children and self.number_of_children is None:
            raise ValidationError("Please specify the number of children.")
        
        # Validate disability information
        if self.is_disabled and not self.disability_details:
            raise ValidationError("Please provide disability accommodation details.")

class User(models.Model):
    """Model representing a restaurant user."""
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)
    has_children = models.BooleanField(default=False)
    number_of_children = models.IntegerField(null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    disability_adjustments = models.TextField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True) 

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username