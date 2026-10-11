from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Visit, Payment
from patients.models import Patient
from prescriptions.models import Prescription, Medicine

@login_required
def visit_list(request):
    visits = Visit.objects.filter(patient__doctor=request.user).select_related('patient').order_by('-visit_date')
    return render(request, 'visits/list.html', {'visits': visits})

@login_required
def visit_create(request):
    doctor = request.user
    patients = Patient.objects.filter(doctor=doctor).order_by('full_name')
    
    # Pre-select patient if provided in URL (e.g., from Patient Detail page)
    selected_patient_id = request.GET.get('patient')
    if selected_patient_id:
        try:
            selected_patient_id = int(selected_patient_id)
        except:
            selected_patient_id = None
            
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = get_object_or_404(Patient, pk=patient_id, doctor=doctor)
        
        consultation_fee = request.POST.get('consultation_fee', 500)
        if not consultation_fee: consultation_fee = 0
        
        visit = Visit.objects.create(
            patient=patient,
            symptoms=request.POST.get('symptoms', ''),
            diagnosis=request.POST.get('diagnosis', ''),
            doctor_notes=request.POST.get('doctor_notes', ''),
            consultation_fee=consultation_fee
        )
        
        Payment.objects.create(visit=visit, amount=consultation_fee)
        
        # Medicines
        medicine_names = request.POST.getlist('medicine_name[]')
        if medicine_names and any(name.strip() for name in medicine_names):
            prescription = Prescription.objects.create(visit=visit)
            for name in medicine_names:
                if name.strip():
                    Medicine.objects.create(
                        prescription=prescription,
                        name=name.strip()
                    )
                    
        return redirect('patient_detail', pk=patient.pk)
        
    return render(request, 'visits/form.html', {
        'patients': patients,
        'selected_patient_id': selected_patient_id
    })
