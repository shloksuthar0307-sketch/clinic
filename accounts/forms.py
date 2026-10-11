from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor

class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    clinic_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Doctor
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'clinic_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.clinic_name = self.cleaned_data['clinic_name']
        if commit:
            user.save()
        return user
