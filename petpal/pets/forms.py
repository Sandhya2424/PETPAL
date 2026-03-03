from django import forms
from pets.models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'age', 'breed', 'gender', 'description', 'image', 'status']
