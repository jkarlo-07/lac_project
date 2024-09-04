# utils.py (in your project-level or app-level directory)
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_contact(name, email, subject, message, to_email, msg_template):
    try:
        html_message = render_to_string(msg_template, {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,  
            email,  
            [to_email],  
            html_message=html_message,  
            fail_silently=False,
        )
        
        return {'success': True, 'message': 'Message has been sent!'}
    
    except BadHeaderError:
        return {'success': False, 'error': 'Invalid header found.'}
    
    except Exception as e:
        return {'success': False, 'error': f'An error occurred: {str(e)}'}
