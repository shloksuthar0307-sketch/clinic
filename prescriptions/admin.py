from django.contrib import admin
from .models import Prescription, Medicine

admin.site.register(Prescription)
admin.site.register(Medicine)
