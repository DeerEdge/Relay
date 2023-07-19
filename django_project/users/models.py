from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    is_online = models.BooleanField()

    def __str__(self):
        return {self.first_name, self.last_name, self.phone_number}

