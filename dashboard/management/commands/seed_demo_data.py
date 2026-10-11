import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from accounts.models import Doctor
from patients.models import Patient
from visits.models import Visit, Payment
from prescriptions.models import Prescription, Medicine

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with demo data for doctors, patients, visits, etc.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create a default doctor
        doctor, created = Doctor.objects.get_or_create(
            username='doctor',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'doctor@example.com',
                'phone': '+1234567890',
                'clinic_name': 'Premium Medical Clinic'
            }
        )
        if created:
            doctor.set_password('password123')
            doctor.save()
            self.stdout.write(f'Created Doctor: {doctor.username} / password123')
        
        # Create Patients
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        symptoms_list = ['Fever', 'Cough', 'Headache', 'Stomach ache', 'Body pain', 'Nausea']
        diagnoses_list = ['Viral Infection', 'Common Cold', 'Migraine', 'Food Poisoning', 'Muscle Strain', 'Gastritis']
        medicines_list = [
            ('Paracetamol', '500mg', '2 times/day', '3 days'),
            ('Vitamin C', '1 tablet', '1 time/day', '7 days'),
            ('Ibuprofen', '400mg', 'As needed', '3 days'),
            ('Amoxicillin', '250mg', '3 times/day', '5 days'),
            ('Omeprazole', '20mg', '1 time/day', '14 days')
        ]

        # Generate 20 patients
        for i in range(20):
            patient = Patient.objects.create(
                doctor=doctor,
                full_name=fake.name(),
                age=random.randint(5, 80),
                gender=random.choice(['Male', 'Female']),
                phone=fake.phone_number()[:20],
                email=fake.email(),
                address=fake.address(),
                blood_group=random.choice(blood_groups),
            )
            
            # Generate 1 to 5 visits per patient
            num_visits = random.randint(1, 5)
            for j in range(num_visits):
                visit_date = timezone.now() - timedelta(days=random.randint(0, 100))
                
                visit = Visit.objects.create(
                    patient=patient,
                    symptoms=random.choice(symptoms_list),
                    diagnosis=random.choice(diagnoses_list),
                    doctor_notes=fake.text(max_nb_chars=100),
                    consultation_fee=random.choice([300, 400, 500, 600])
                )
                
                # Override auto_now_add for visit_date
                Visit.objects.filter(id=visit.id).update(visit_date=visit_date)
                
                # Payment
                Payment.objects.create(
                    visit=visit,
                    amount=visit.consultation_fee,
                )
                
                # Prescription
                if random.choice([True, False]): # 50% chance of prescription
                    prescription = Prescription.objects.create(visit=visit)
                    Prescription.objects.filter(id=prescription.id).update(created_at=visit_date)
                    
                    num_meds = random.randint(1, 3)
                    for k in range(num_meds):
                        med = random.choice(medicines_list)
                        Medicine.objects.create(
                            prescription=prescription,
                            name=med[0],
                            dosage=med[1],
                            frequency=med[2],
                            duration=med[3],
                            instructions="Take after food."
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
