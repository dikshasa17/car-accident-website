from django.forms import ModelForm
from .models import Accident
from .models import Emergency
class Accidentform(ModelForm):
    class Meta:
        model = Accident
        fields = [
                  'user_name',
                  'user_mobile',
                  'user_email',
                  'image',
                  'vehicle_number_plate',
                  'address',
                  'bloodgrp',
                  'emergency_no1',
                  'emergency_no2'    
                  ]

class EmergencyForm(ModelForm):
    class Meta:
        model = Emergency
        fields = [
                  'form_filler_name',
                  'mobile_no',
                  'accident_vehicle_number',
                  'accident_image',
                  'location_link',
                  ]