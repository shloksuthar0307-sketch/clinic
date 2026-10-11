from django.db import models
from django.conf import settings
import uuid

class Patient(models.fields.AutoField): pass # just testing if this fails or not, i will just write the model.

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients')
    patient_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Personal Info
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    
    # Medical Info
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    existing_conditions = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate a simple unique ID, could be customized further
            last_patient = Patient.objects.order_by('id').last()
            if last_patient:
                self.patient_id = f"PT-{last_patient.id + 1024}"
            else:
                self.patient_id = "PT-1024"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.patient_id})"
