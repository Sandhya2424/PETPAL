from django import forms
from adoption.models import AdoptionRequest

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['full_name', 'email', 'phone', 'address', 'reason']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Your Address', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why do you want to adopt this pet?', 'class': 'form-control'}),
        }
