from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from hospital.models import Hospital, Patient, DrugAdmin, Doctor

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'is_active', 'is_superadmin')

# 角色表单
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('hospital', 'name', 'department', 'title', 'contact')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'gender', 'birth', 'contact', 'address')

class DrugAdminForm(forms.ModelForm):
    class Meta:
        model = DrugAdmin
        fields = ('hospital', 'name')