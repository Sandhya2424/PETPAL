from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
