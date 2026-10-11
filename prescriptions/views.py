from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Prescription, Medicine
from visits.models import Visit, Payment
from patients.models import Patient

@login_required
def prescription_list(request):
    doctor = request.user
    prescriptions = Prescription.objects.filter(visit__patient__doctor=doctor).select_related('visit__patient').order_by('-created_at')
    
    return render(request, 'prescriptions/list.html', {'prescriptions': prescriptions})

@login_required
def prescription_detail(request, pk):
    doctor = request.user
    prescription = get_object_or_404(Prescription, pk=pk, visit__patient__doctor=doctor)
    return render(request, 'prescriptions/detail.html', {'prescription': prescription})

@login_required
def prescription_create(request):
    doctor = request.user
    patients = Patient.objects.filter(doctor=doctor).order_by('full_name')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        diagnosis = request.POST.get('diagnosis', 'General Consultation')
        
        patient = get_object_or_404(Patient, pk=patient_id, doctor=doctor)
        
        # Create a new visit for this prescription
        visit = Visit.objects.create(
            patient=patient,
            diagnosis=diagnosis,
            symptoms='Not specified',
            consultation_fee=0 # Free/Follow-up by default for standalone prescription
        )
        Payment.objects.create(visit=visit, amount=0)
        
        prescription = Prescription.objects.create(visit=visit)
        
        # Handle medicines
        medicine_names = request.POST.getlist('medicine_name[]')
        dosages = request.POST.getlist('medicine_dosage[]')
        frequencies = request.POST.getlist('medicine_frequency[]')
        durations = request.POST.getlist('medicine_duration[]')
        instructions_list = request.POST.getlist('medicine_instructions[]')
        
        for i, name in enumerate(medicine_names):
            if name.strip():
                Medicine.objects.create(
                    prescription=prescription,
                    name=name.strip(),
                    dosage=dosages[i] if i < len(dosages) else '',
                    frequency=frequencies[i] if i < len(frequencies) else '',
                    duration=durations[i] if i < len(durations) else '',
                    instructions=instructions_list[i] if i < len(instructions_list) else ''
                )
                
        return redirect('prescription_list')

    return render(request, 'prescriptions/form.html', {'patients': patients})

@login_required
def prescription_edit(request, pk):
    doctor = request.user
    prescription = get_object_or_404(Prescription, pk=pk, visit__patient__doctor=doctor)
    
    if request.method == 'POST':
        # Update diagnosis if provided
        diagnosis = request.POST.get('diagnosis')
        if diagnosis:
            prescription.visit.diagnosis = diagnosis
            prescription.visit.save()
            
        # Delete existing medicines and recreate
        prescription.medicines.all().delete()
        
        medicine_names = request.POST.getlist('medicine_name[]')
        dosages = request.POST.getlist('medicine_dosage[]')
        frequencies = request.POST.getlist('medicine_frequency[]')
        durations = request.POST.getlist('medicine_duration[]')
        instructions_list = request.POST.getlist('medicine_instructions[]')
        
        for i, name in enumerate(medicine_names):
            if name.strip():
                Medicine.objects.create(
                    prescription=prescription,
                    name=name.strip(),
                    dosage=dosages[i] if i < len(dosages) else '',
                    frequency=frequencies[i] if i < len(frequencies) else '',
                    duration=durations[i] if i < len(durations) else '',
                    instructions=instructions_list[i] if i < len(instructions_list) else ''
                )
                
        return redirect('prescription_list')
        
    return render(request, 'prescriptions/form.html', {'prescription': prescription})

@login_required
def prescription_delete(request, pk):
    doctor = request.user
    prescription = get_object_or_404(Prescription, pk=pk, visit__patient__doctor=doctor)
    
    if request.method == 'POST':
        prescription.delete()
        return redirect('prescription_list')
        
    # fallback if accessed via GET
    return redirect('prescription_list')
