from django import forms
from .models import PreTest

class PreTestForm(forms.ModelForm):
    class Meta:
        model = PreTest
        exclude = ['student', 'bmi', 'vo2_max']
        widgets = {
            'date_of_pretest': forms.DateInput(attrs={'type': 'date'}),
        }
