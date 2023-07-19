from django.db import models

# Create your models here.

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    date_joined = models.DateTimeField(null=True)
    int_phone = models.IntegerField(null=True)
    def __str__(self):
        return {self.phone_number, self.name, self.date_joined, self.int_phone}

