from django.core.management.base import BaseCommand
from content.models import RoomType 
from datetime import datetime

class Command(BaseCommand):
    help = 'Update the prices of all RoomType entries based on seasonal multipliers'

    def handle(self, *args, **kwargs):
        test_date = datetime.now() 
        room_types = RoomType.objects.all()
        updated_count = 0  

        for room_type in room_types:

            seasonal_price = room_type.get_seasonal_price(test_date)
            
            room_type.price = seasonal_price
            print(room_type.price)
            room_type.save()
            print(room_type.price)
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated prices for {updated_count} room type(s).'))
