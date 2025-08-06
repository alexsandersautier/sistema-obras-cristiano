from django import forms
from .models import Building, Template

class BuildingFormAdmin(forms.ModelForm):
    
    template = forms.ModelChoiceField(
        queryset=Template.objects.all(),
        required=False,
        label='Template'
    )
    
    class Meta:
        model = Building
        fields = '__all__'