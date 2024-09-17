from django.contrib import admin
from .models import RoomType
from .models import Room
# Register your models here.

admin.site.register(RoomType)
admin.site.register(Room)