from django.urls import path
from . import views

urlpatterns = [
    path('', views.visit_list, name='visit_list'),
    path('add/', views.visit_create, name='visit_create'),
]
