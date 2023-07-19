from django.db import models
from users.models import Customer

# Create your models here.

class Message(models.Model):
    sender_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    read = models.BooleanField(null=True)
    message_body = models.TextField(null=True)

    def __str__(self):
        return {self.sender_id, self.receiver_id, self.read, self.message_body}


