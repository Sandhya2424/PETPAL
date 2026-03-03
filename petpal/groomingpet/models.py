from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('Basic', 'Basic'),
        ('Basic + Hygiene', 'Basic + Hygiene'),
        ('Essential', 'Essential'),
        ('Advance', 'Advance'),
        ('Haircut', 'Haircut'),
    ]

    adopter = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=50)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    # ⭐ Fields for payment system
    payment_method = models.CharField(max_length=20, null=True, blank=True)  # "online" or "cod"
    order_id = models.CharField(max_length=100, null=True, blank=True)       # Razorpay order ID OR COD_ID
    amount = models.IntegerField(null=True, blank=True)                       # Total price
    is_paid = models.BooleanField(default=False)                              # Payment status

    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.adopter.username} - {self.service} - {self.date}"

