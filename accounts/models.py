from django.db import models
from django.contrib.auth.models import AbstractUser

class Doctor(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    clinic_name = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}" if self.first_name else self.username
