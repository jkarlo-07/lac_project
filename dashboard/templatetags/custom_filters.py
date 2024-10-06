from django import template
from datetime import date

register = template.Library()

@register.filter
def age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
