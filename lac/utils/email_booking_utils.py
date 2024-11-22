# utils.py (in your project-level or app-level directory)
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from content.models import Booking
from django.shortcuts import get_object_or_404

def send_booking_details(name, email, subject, to_email, msg_template, book_id):
    try:
        booking = get_object_or_404(Booking, id=book_id)
        num_guests = booking.adult_count + booking.kid_count
        if booking.is_overnight:
            entrance_fee =(float(100)*float(booking.kid_count)) + (float(150)*float(booking.adult_count))
            entrance_prompt = "(Adult: ₱150, Kid:₱100)"
        else:
            entrance_fee =(float(50)*float(booking.kid_count)) + (float(100)*float(booking.adult_count))
            entrance_prompt = "(Adult: ₱100, Kid:₱50)"
        html_message = render_to_string(msg_template, {
            'name': name,
            'email': email,
            'subject': subject,
            'book_id': book_id,
            'name': booking.guest.first_name,
            'check_in': booking.check_in,
            'check_out': booking.check_out,
            'num_guests': num_guests,
            'room_type': booking.room.room_type,
            'room_number': booking.room.room_number,
            'room_amount': booking.room.room_type.price,
            'adult_count': booking.adult_count,
            'kid_count': booking.kid_count,
            'entrance_fee': entrance_fee,
            'total_amount': booking.total_amount,
            'entrance_prompt': entrance_prompt,
        })
        
        plain_message = strip_tags(html_message)
        
        user_email = booking.guest.user.email

        send_mail(
            subject,
            plain_message,  
            email,  
            [user_email],  
            html_message=html_message,  
            fail_silently=False,
        )
        
        return {'success': True, 'message': 'Message has been sent!'}
    
    except BadHeaderError:
        return {'success': False, 'error': 'Invalid header found.'}
    
    except Exception as e:
        return {'success': False, 'error': f'An error occurred: {str(e)}'}
