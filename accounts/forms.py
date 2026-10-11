from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Doctor

class DoctorSignUpForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    clinic_name = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = Doctor
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'clinic_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data and 'password' not in self.data and 'password1' in self.data:
            self.data = self.data.copy()
            self.data['password'] = self.data.get('password1')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.clinic_name = self.cleaned_data['clinic_name']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
