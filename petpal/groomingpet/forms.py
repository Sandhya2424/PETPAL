from django import forms
from groomingpet.models import Appointment

# ----------------------------
# Appointment Form
# ----------------------------
TIME_SLOTS = [
    '9:00 AM – 10:00 AM',
    '10:30 AM – 11:30 AM',
    '12:00 PM – 1:00 PM',
    '1:30 PM – 2:30 PM',
    '3:00 PM – 4:00 PM',
    '4:30 PM – 5:30 PM',
    '6:00 PM – 7:00 PM',
]

class AppointmentForm(forms.ModelForm):
    time_slot = forms.ChoiceField(
        choices=[(t, t) for t in TIME_SLOTS],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Appointment
        fields = ['pet_name', 'pet_type', 'date', 'time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pet_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        if date and time_slot:
            count = Appointment.objects.filter(date=date, time_slot=time_slot).count()
            if count >= 5:
                raise forms.ValidationError(
                    f"The slot {time_slot} on {date} is fully booked. Please choose another slot."
                )
        return cleaned_data

# ----------------------------
# Payment Form
# ----------------------------
class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ("online", "Online Payment"),
        ("cod", "Cash on Delivery"),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
