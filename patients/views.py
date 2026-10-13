from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient
from visits.models import Visit, Payment
from prescriptions.models import Prescription, Medicine
from django.db.models import Count, Q, Max, Sum
from .forms import PatientForm

@login_required
def patient_list(request):
    doctor = request.user
    
    # Base query with aggregate data
    patients = Patient.objects.filter(doctor=doctor).annotate(
        visit_count=Count('visits'),
        last_visit=Max('visits__visit_date'),
        total_paid=Sum('visits__payments__amount')
    ).order_by('-created_at')
    
    # Search
    query = request.GET.get('q')
    if query:
        patients = patients.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(patient_id__icontains=query)
        )
        
    # Filter by visit count (Returning filter)
    visits_filter = request.GET.get('visits')
    if visits_filter:
        try:
            val = int(visits_filter.replace('+', ''))
            if '+' in visits_filter:
                patients = patients.filter(visit_count__gte=val)
            else:
                patients = patients.filter(visit_count=val)
        except ValueError:
            pass

    context = {
        'patients': patients,
        'search_query': query,
        'visits_filter': visits_filter
    }
    return render(request, 'patients/list.html', context)

@login_required
def add_patient(request):
    if request.method == 'POST':
        # Parse all data manually to handle complex nested forms
        
        # 1. Patient Info
        patient = Patient.objects.create(
            doctor=request.user,
            full_name=request.POST.get('full_name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            phone=request.POST.get('phone'),

            # Optional medical info
            blood_group=request.POST.get('blood_group', '').strip(),
            allergies=request.POST.get('allergies', '').strip(),
            existing_conditions=request.POST.get('existing_conditions', '').strip(),
            medical_history=request.POST.get('medical_history', '').strip(),
            emergency_contact=request.POST.get('emergency_contact', '').strip()
        )
        
        consultation_fee = request.POST.get('consultation_fee')
        if consultation_fee:
            amount_paid = request.POST.get('amount_paid', 0)
            if not amount_paid: amount_paid = 0
            
            visit = Visit.objects.create(
                patient=patient,
                symptoms='Initial Registration',
                diagnosis=request.POST.get('diagnosis', 'N/A'),
                treatment=request.POST.get('treatment', ''),
                consultation_fee=consultation_fee
            )
            Payment.objects.create(visit=visit, amount=amount_paid)
            
            # Process Prescriptions
            med_names = request.POST.getlist('medicine_name[]')
            
            if any(name.strip() for name in med_names):
                prescription = Prescription.objects.create(visit=visit)
                for name in med_names:
                    if name.strip():
                        Medicine.objects.create(
                            prescription=prescription,
                            name=name.strip(),
                            dosage='',
                            frequency='',
                            duration='',
                            instructions=''
                        )
            
        return redirect('patient_detail', pk=patient.pk)
        
    return render(request, 'patients/add.html')

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, doctor=request.user)
    visits = patient.visits.all().order_by('-visit_date')
    
    total_paid = patient.visits.aggregate(Sum('payments__amount'))['payments__amount__sum'] or 0
    avg_fee = total_paid / visits.count() if visits.count() > 0 else 0
    
    context = {
        'patient': patient,
        'visits': visits,
        'total_paid': total_paid,
        'avg_fee': avg_fee
    }
    return render(request, 'patients/detail.html', context)

@login_required
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk, doctor=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        if full_name:
            patient.full_name = full_name
            
        age = request.POST.get('age')
        if age:
            try:
                patient.age = int(age)
            except ValueError:
                pass
                
        gender = request.POST.get('gender')
        if gender:
            patient.gender = gender
            
        phone = request.POST.get('phone', '').strip()
        if phone:
            patient.phone = phone
            
        patient.blood_group = request.POST.get('blood_group', '').strip()
        patient.emergency_contact = request.POST.get('emergency_contact', '').strip()
        patient.allergies = request.POST.get('allergies', '').strip()
        patient.existing_conditions = request.POST.get('existing_conditions', '').strip()
        patient.medical_history = request.POST.get('medical_history', '').strip()
        
        patient.save()
        messages.success(request, f"Patient {patient.full_name}'s profile has been updated successfully.")
        return redirect('patient_detail', pk=patient.pk)
        
    return render(request, 'patients/edit.html', {'patient': patient})

@login_required
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk, doctor=request.user)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient_list')
    return redirect('patient_detail', pk=pk)
