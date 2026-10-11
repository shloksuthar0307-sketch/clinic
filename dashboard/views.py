from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from patients.models import Patient
from visits.models import Visit, Payment
from django.http import JsonResponse
from datetime import timedelta

@login_required
def dashboard_view(request):
    doctor = request.user
    today = timezone.now().date()
    
    # Base querysets
    patients_qs = Patient.objects.filter(doctor=doctor)
    visits_qs = Visit.objects.filter(patient__doctor=doctor)
    
    # Stats
    total_patients = patients_qs.count()
    
    todays_visits = visits_qs.filter(visit_date__date=today)
    todays_patients = todays_visits.values('patient').distinct().count()
    
    todays_revenue = Payment.objects.filter(
        visit__patient__doctor=doctor, 
        paid_date__date=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    first_day_of_month = today.replace(day=1)
    monthly_revenue = Payment.objects.filter(
        visit__patient__doctor=doctor, 
        paid_date__date__gte=first_day_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Returning patients (patients with > 1 visit)
    returning_patients = patients_qs.annotate(visit_count=Count('visits')).filter(visit_count__gt=1).count()
    
    # Recent visits
    recent_visits = visits_qs.select_related('patient').order_by('-visit_date')[:5]
    
    context = {
        'total_patients': total_patients,
        'todays_patients': todays_patients,
        'todays_revenue': todays_revenue,
        'monthly_revenue': monthly_revenue,
        'returning_patients': returning_patients,
        'recent_visits': recent_visits,
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def chart_data_api(request):
    doctor = request.user
    today = timezone.now().date()
    
    # Last 7 days revenue
    labels = []
    revenue_data = []
    visits_data = []
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        labels.append(date.strftime('%b %d'))
        
        # Revenue for the day
        daily_rev = Payment.objects.filter(
            visit__patient__doctor=doctor,
            paid_date__date=date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        revenue_data.append(float(daily_rev))
        
        # Visits for the day
        daily_vis = Visit.objects.filter(
            patient__doctor=doctor,
            visit_date__date=date
        ).count()
        visits_data.append(daily_vis)
        
    return JsonResponse({
        'labels': labels,
        'revenue': revenue_data,
        'visits': visits_data
    })
