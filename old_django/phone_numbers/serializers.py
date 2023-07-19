from rest_framework import serializers
from .models import *

class PhoneNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'