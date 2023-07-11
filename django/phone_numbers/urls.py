from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_phone_numbers, name='All Phone Numbers'),
    path('add/', views.add_phone_number, name='Add Phone Number'),

]