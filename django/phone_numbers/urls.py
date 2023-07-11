from django.urls import path
from . import views
from .views import PhoneNumberDetail

urlpatterns = [
    path('', views.all_phone_numbers, name='All Phone Numbers'),
    path('add/', views.add_phone_number, name='Add Phone Number'),
    path('nums/<int:pk>/', PhoneNumberDetail.as_view()),

]