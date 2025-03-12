from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime

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
    
    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"
    