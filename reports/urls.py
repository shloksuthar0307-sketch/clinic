from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_view, name='reports'),
    path('export/patients/', views.export_patients_excel, name='export_patients'),
    path('export/visits/', views.export_visits_excel, name='export_visits'),
]
