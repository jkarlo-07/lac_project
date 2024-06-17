from django.db import models

# Create your models here.

class RoomType(models.Model):
    room_type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='room/', default='room/room_fallback.jpg', blank=True)

    def __str__(self):
        return self.room_type
    
