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

    def __str__(self):
        return self.room_type
    
class Room(models.Model):
    room_number = models.CharField(max_length=50)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE) 

    def __str__(self):
        return self.room_number
    
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    start_time = models.TimeField(default=time(8, 0))
    end_time = models.TimeField(default=time(20, 0))
    duration = models.DurationField(default=timedelta(hours=12)) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def room_number(self):
        return self.room.room_number
    
    
