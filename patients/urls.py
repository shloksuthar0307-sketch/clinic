from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.add_patient, name='add_patient'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:pk>/delete/', views.delete_patient, name='delete_patient'),
]
