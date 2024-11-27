from django.core.management.base import BaseCommand
from content.models import Booking, SeasonalData
from django.db import models
from django.db.models import Count
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Analyze historical booking data from the last 2 years to determine peak and off-peak seasons'

    def handle(self, *args, **kwargs):
        two_years_ago = datetime.now() - timedelta(days=365*2)


        bookings_per_month = Booking.objects.filter(check_in__gte=two_years_ago).annotate(
            month=models.functions.ExtractMonth('check_in')
        ).values('month').annotate(total_bookings=Count('id')).order_by('month')


        total_bookings = sum(b['total_bookings'] for b in bookings_per_month)
        average_bookings = total_bookings / len(bookings_per_month) if bookings_per_month else 0

        peak_months = [entry['month'] for entry in bookings_per_month if entry['total_bookings'] > average_bookings * 1.5]
        off_peak_months = [entry['month'] for entry in bookings_per_month if entry['total_bookings'] < average_bookings * 0.8]

        current_year = datetime.now().year
        years_range = list(range(current_year - 1, current_year + 1))  

        seasonal_data, created = SeasonalData.objects.get_or_create(years=years_range)

        seasonal_data.peak_months = peak_months
        seasonal_data.off_peak_months = off_peak_months
        seasonal_data.save()

        self.stdout.write(self.style.SUCCESS(f"Seasonal data for {years_range[0]}-{years_range[-1]} saved successfully!"))
