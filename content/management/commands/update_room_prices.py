from django.core.management.base import BaseCommand
from content.models import RoomType  # Make sure to import RoomType from the correct app
from datetime import datetime

class Command(BaseCommand):
    help = 'Update the prices of all RoomType entries based on seasonal multipliers'

    def handle(self, *args, **kwargs):
        # Set a fixed date for testing (e.g., June 15th, 2024)
        test_date = datetime.now() # June 15, 2024
        print(test_date)
        # Loop through all RoomType entries
        room_types = RoomType.objects.all()
        updated_count = 0  # To keep track of how many rooms have been updated

        for room_type in room_types:
            # Calculate the seasonal price for each room_type based on the test check-in date (June 15th)
            seasonal_price = room_type.get_seasonal_price(test_date)
            
            # Update the price field with the seasonal price
            room_type.price = seasonal_price
            print(room_type.price)
            room_type.save()
            print(room_type.price)
            updated_count += 1

        # Output the success message
        self.stdout.write(self.style.SUCCESS(f'Successfully updated prices for {updated_count} room type(s).'))
