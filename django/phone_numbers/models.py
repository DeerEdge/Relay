from django.db import models

# Create your models here.

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=200)
    def __str__(self):
        return self.phone_number

