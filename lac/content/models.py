from django.db import models

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
    
