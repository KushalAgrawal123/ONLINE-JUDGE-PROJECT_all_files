from django import forms
from .models import Problem, Testcase

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title','slug','statement','time_limit','memory_limit']

class TestcaseForm(forms.ModelForm):
    class Meta:
        model = Testcase
        fields = ['order','input_data','expected_output','is_sample']
        widgets = {
            'input_data':    forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
            'expected_output': forms.Textarea(attrs={'rows':2, 'class':'form-control'}),
            'order': forms.NumberInput(attrs={'class':'form-control','min':0}),
            'is_sample': forms.CheckboxInput(),
        }
