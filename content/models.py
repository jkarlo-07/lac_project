from django.db import models
from users.models import CustomUser
from datetime import timedelta, time
# Create your models here.

class RoomType(models.Model):
    room_type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='room/', default='room/room_fallback.jpg', blank=True)
    is_cottage_required = models.BooleanField(default=True)
    cottage_price = models.DecimalField(max_digits=10, decimal_places=2, default=750)

    def __str__(self):
        return self.room_type
    
class Room(models.Model):
    room_number = models.CharField(max_length=50)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE) 

    def __str__(self):
        return self.room_number
    
class Guest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    date_of_birth = models.DateField(default="2002-01-01")
    
    def __str__(self):
        return self.first_name




class TempGuest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    date_of_birth = models.DateField(default="2002-01-01")
    
    def __str__(self):
        return self.first_name
    
class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)  # Allow NULL values
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=12))
    adult_count = models.IntegerField(default=1)
    kid_count = models.IntegerField(default=0)
    is_overnight = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
   

    @property
    def room_number(self):
        return self.room.room_number if self.room else "Room deleted"
    
    
