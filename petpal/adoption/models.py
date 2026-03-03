from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet

class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, default='N/A')
    email = models.EmailField(default='N/A')
    phone = models.CharField(max_length=20, default='N/A')
    address = models.TextField(default='N/A')
    reason = models.TextField(default='N/A')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.pet.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"
