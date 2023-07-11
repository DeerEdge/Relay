from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *

# Create your views here.
@api_view(['GET'])
def all_phone_numbers(request):
    phone_numbers = PhoneNumber.objects.all()
    serializer = PhoneNumbersSerializer(phone_numbers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_phone_number(request):
    data = request.data
    serializer = PhoneNumbersSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)