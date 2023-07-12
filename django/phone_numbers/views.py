from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import generics
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

class PhoneNumberList(generics.ListCreateAPIView):
    serializer_class = PhoneNumbersSerializer

    def get_queryset(self):
        queryset = PhoneNumber.objects.all()
        phone_number = self.request.query_params.get('phone_number')
        if phone_number is not None:
            queryset = queryset.filter(phone_number=phone_number)
        return queryset

class PhoneNumberDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhoneNumbersSerializer
    queryset = PhoneNumber.objects.all()