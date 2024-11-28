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
            month=models.functions.ExtractMonth('check_in'),
            year=models.functions.ExtractYear('check_in')
        ).values('month', 'year').annotate(total_bookings=Count('id')).order_by('month', 'year')

        bookings_by_month = {}

        for entry in bookings_per_month:
            month = entry['month']
            year = entry['year']
            total_bookings = entry['total_bookings']
            
            if month not in bookings_by_month:
                bookings_by_month[month] = []
            
            bookings_by_month[month].append(total_bookings)

        total_bookings = sum(sum(bookings) for bookings in bookings_by_month.values())
        total_months = sum(len(bookings) for bookings in bookings_by_month.values())
        average_bookings = total_bookings / total_months if total_months else 0

        peak_months = []
        off_peak_months = []

        for month, bookings in bookings_by_month.items():
            normalized_average = sum(bookings) / len(bookings)
            print(month, normalized_average)
            if normalized_average > average_bookings * 1.5:
                peak_months.append(month)

            elif normalized_average < average_bookings * 0.8:
                off_peak_months.append(month)

        current_year = datetime.now().year
        years_range = list(range(current_year - 1, current_year + 1))

        seasonal_data, created = SeasonalData.objects.get_or_create(years=years_range)

        seasonal_data.peak_months = peak_months
        seasonal_data.off_peak_months = off_peak_months
        seasonal_data.save()

        self.stdout.write(self.style.SUCCESS(f"Seasonal data for {years_range[0]}-{years_range[-1]} saved successfully!"))
