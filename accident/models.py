from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Accident(models.Model):
    user_name=models.CharField(max_length=20)
    user_mobile=models.CharField(max_length=10)
    user_email=models.EmailField()
    vehicle_number_plate =models.CharField(max_length=20)
    address= models.TextField(max_length=100)
    bloodgrp= models.CharField(max_length=6)
    image = models.ImageField(upload_to='accident/images/',blank=False)
    emergency_no1=models.CharField(max_length=10)
    emergency_no2=models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name

class Emergency(models.Model):
    form_filler_name=models.CharField(max_length=20)
    mobile_no=models.CharField(max_length=10)
    accident_vehicle_number = models.CharField(max_length=20)
    accident_image = models.ImageField(upload_to='accident/images/',blank=False)
    location_link= models.URLField(blank=True)
    

    def __str__(self):
        return self.accident_vehicle_number 
    
   