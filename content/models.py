from django.db import models
from users.models import CustomUser
from datetime import timedelta, time, datetime
# Create your models here.

from decimal import Decimal

class RoomType(models.Model):
    room_type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=1500)  # Original price
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Adjusted price
    capacity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='room/', default='room/room_fallback.jpg', blank=True)
    is_cottage_required = models.BooleanField(default=True)
    cottage_price = models.DecimalField(max_digits=10, decimal_places=2, default=750)

    def __str__(self):
        return self.room_type

    def get_seasonal_multiplier(self, check_in):
        current_year = check_in.year
        years_range = [current_year - 1, current_year]  

        try:
            seasonal_data = SeasonalData.objects.get(years=years_range)
            peak_months = seasonal_data.peak_months
            off_peak_months = seasonal_data.off_peak_months
        except SeasonalData.DoesNotExist:
            peak_months = []
            off_peak_months = []

        month = check_in.month

        if month in peak_months:
            return Decimal('1.1')  
        else:
            return Decimal('1')  # Convert the multiplier to Decimal

    def get_seasonal_price(self, check_in):
        multiplier = self.get_seasonal_multiplier(check_in)
        seasonal_price = self.base_price * multiplier  # This will now work with Decimal
        
        if self.is_cottage_required:
            seasonal_price += self.cottage_price
        
        return seasonal_price

    
class Room(models.Model):
    room_number = models.CharField(max_length=50)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE) 

    def __str__(self):
        return self.room_number
    
class Guest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75, blank=True)  
    address = models.CharField(max_length=200, blank=True) 
    phone = models.CharField(max_length=30, blank=True)  
    date_of_birth = models.DateField(blank=True, null=True)  
    
    def __str__(self):
        return self.first_name




class TempGuest(models.Model):
    user = models.IntegerField()
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    date_of_birth = models.DateField(default="2002-01-01")
    room = models.IntegerField(default=1)  
    check_in = models.DateTimeField(default=datetime(2024, 1, 1, 8, 0))
    check_out = models.DateTimeField(default=datetime(2024, 1, 1, 8, 0))
    duration = models.DurationField(default=timedelta(hours=12))
    adult_count = models.IntegerField(default=1)
    kid_count = models.IntegerField(default=0)
    is_overnight = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    
    def __str__(self):
        return self.first_name
    
class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)  # Allow NULL values
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.CharField(max_length=10, default="Booked")
    duration = models.DurationField(default=timedelta(hours=12))
    adult_count = models.IntegerField(default=1)
    kid_count = models.IntegerField(default=0)
    is_overnight = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_method = models.CharField(max_length=15, default="online")
   

    @property
    def room_number(self):
        return self.room.room_number if self.room else "Room deleted"
    
    
from django.db import models
import json

from django.db import models

class SeasonalData(models.Model):
    years = models.JSONField(default=list)
    peak_months = models.JSONField(default=list)  # Store peak months
    off_peak_months = models.JSONField(default=list)  # Store off-peak months

    def __str__(self):
        # Convert list of years to a range like "2022-2024"
        years_range = f"{min(self.years)}-{max(self.years)}" if self.years else "Unknown"
        return f"Seasonal Data for {years_range}"

