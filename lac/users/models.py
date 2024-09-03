from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email_confirm_code = models.CharField(max_length=4, blank=True, null=True)
