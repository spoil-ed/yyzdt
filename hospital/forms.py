from django import forms
from .models import Hospital, HospitalGrade, HospitalType, City

class HospitalForm(forms.ModelForm):
    """医院表单"""
    class Meta:
        model = Hospital
        fields = ['name', 'grade', 'type', 'city', 'address', 'contact', 'email', 'description', 'founded']
        
        widgets = {
            'founded': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].queryset = HospitalGrade.objects.all()
        self.fields['type'].queryset = HospitalType.objects.all()
        self.fields['city'].queryset = City.objects.all()