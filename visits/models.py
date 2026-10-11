from django.db import models
from patients.models import Patient

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.CharField(max_length=255)
    treatment = models.CharField(max_length=255, blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    
    @property
    def has_prescription(self):
        return hasattr(self, 'prescription')
        
    @property
    def total_paid(self):
        return self.payments.aggregate(models.Sum('amount'))['amount__sum'] or 0
        
    @property
    def due(self):
        return max(0, self.consultation_fee - self.total_paid)
        
    def __str__(self):
        return f"Visit on {self.visit_date.strftime('%Y-%m-%d')} for {self.patient.full_name}"

class Payment(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.visit}"
