from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from rest_framework.decorators import api_view
from django.http import JsonResponse
import pyrebase

# Configure below firebase connection
firebaseConfig = {

}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Authentication
auth = firebase.auth()

# Storage. Stored like drive.
storage = firebase.storage()

def home(request):
    return render(request,"accident/home.html")

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'accident/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('userdetail')
            except IntegrityError:
                return render(request, 'accident/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'accident/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'accident/loginuser.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accident/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def userdetail(request):
  
    if request.method == 'GET':
        return render(request, 'accident/userdetail.html')
    else: 
        user = db.child("users").order_by_child("username").equal_to(request.user.username).limit_to_first(1).get()
        if user.val():
            return render(request, 'accident/viewdetails.html', {'msg': "You've already filled the form."})
        else:
            file= request.FILES['img']
            file_format = file.name.split('.')[-1] 
            fireb_upload = storage.child(f"users_image/{request.user}.{file_format}").put(file)
            image_url=storage.child(f"users_image/{request.user}.{file_format}").get_url(None)

            # Setting a default location, so not saving location of user for now. You can change it.
            data = {
                "username":request.user.username,
                "full_name":request.POST['full-name'],
                "email":request.POST['email'],
                "mobile_no":request.POST['mobile-no'],
                "vehicle_number_plate":request.POST['vehicle-number-plate'],
                "address":request.POST['address'],
                "bloodgrp": request.POST['blood-group'],
                "emergency_no1":request.POST['emergency-no-1'],
                "emergency_no2":request.POST['emergency-no-2'],
                "user_image_url":image_url,
                "user_image_token": fireb_upload['downloadTokens'],
                "seatbelt_on":False,
                "alcohol_detected":False,
                "collision_detected":False,
                "vib_sensor_on": False,
                "flame_detected":False,
            }
            # Storing fire_sensor_datetimestamps in lists because we want it to be ordered by entry datetime stamps (as we'll be pushing and popping)
            
            # Saving with custom id: username
            db.child("users").child(request.user).set(data)

            return redirect('viewdetails')
            
def viewdetails(request):
    if request.user.is_superuser == True:
        users_list=[]
        users = db.child("users").order_by_child("username").get()
        if users.val():
            for user in users.each():
                users_list.append(user.val())
        # users_list is stored in this format now: [{'address': 'New address', 'bloodgrp': 'AB+', 'email': 'diksha@gmail.com',...},{...}]

        return render(request, 'accident/adminuser.html', {'users_list': users_list})
    else:
        user_details = db.child("users").order_by_child("username").equal_to(request.user.username).limit_to_first(1).get()
        if user_details.val():
            user_details=user_details.val()
            for k, v in user_details.items():
                user_details=v
        
        # user_details is stored in this format now: {'address': 'New address', 'bloodgrp': 'AB+', 'email': 'diksha@gmail.com',...}
            return render(request, 'accident/viewdetails.html', {'user_details': user_details})
        else:
            return render(request, 'accident/viewdetails.html')

def deletedetails(request):
    if request.method == 'POST':
        try:
            user_details = db.child("users").order_by_child("username").equal_to(request.user.username).limit_to_first(1).get()
            if user_details.val():
                user_details=user_details.val()
                for k, v in user_details.items():
                    user_details=v
            file_format = user_details['user_image_url'].split(".")[-1].split("?")[0]
            # Deleting data from storage database
            storage.delete(f"users_image/{request.user}.{file_format}",user_details['user_image_token'])
            # Deleting data from realtime database
            db.child("users").child(request.user.username).remove()
            return render(request, 'accident/viewdetails.html', {'msgs': "Your details have been successfully deleted!"})
        
        except:
            return render(request, 'accident/viewdetails.html', {'msgs': "Some server error occurred while deleting the details!"})

def editdetails(request):
    user_details = db.child("users").order_by_child("username").equal_to(request.user.username).limit_to_first(1).get()
    user_details=user_details.val()
    for k, v in user_details.items():
        user_details=v

    if request.method == 'GET':
        return render(request,'accident/editdetails.html',{'user_details': user_details})
    
    elif request.method == 'POST':        
        try:
            file= request.FILES['img']
        except:
            return render(request,'accident/editdetails.html',{'user_details': user_details,'error': "No file was selected"})
        file_format = file.name.split('.')[-1] 
        # Replacement won't be done if extensions of image are different so:
        # Deleting previous image file:
        user_details = db.child("users").order_by_child("username").equal_to(request.user.username).limit_to_first(1).get()
        if user_details.val():
            user_details=user_details.val()
            for k, v in user_details.items():
                user_details=v
        prev_file_format = user_details['user_image_url'].split(".")[-1].split("?")[0]
        storage.delete(f"users_image/{request.user}.{prev_file_format}",user_details['user_image_token'])
        
        # Uploading new image file
        fireb_upload = storage.child(f"users_image/{request.user}.{file_format}").put(file)
        image_url=storage.child(f"users_image/{request.user}.{file_format}").get_url(None)
        
        data = {
            "username":request.user.username,
            "full_name": request.POST['full-name'],
            "email":request.POST['email'],
            "mobile_no":request.POST['mobile-no'],
            "vehicle_number_plate":request.POST['vehicle-number-plate'],
            "address":request.POST['address'],
            "bloodgrp": request.POST['blood-group'],
            "emergency_no1":request.POST['emergency-no-1'],
            "emergency_no2":request.POST['emergency-no-2'],
            "user_image_url":image_url,
            "user_image_token": fireb_upload['downloadTokens'],
            "seatbelt_on":user_details['seatbelt_on'],
            "alcohol_detected":user_details['alcohol_detected'],
            "collision_detected":user_details['collision_detected'],
            "vib_sensor_on":user_details['vib_sensor_on'],
            "flame_detected":user_details['flame_detected'],
        }
        
        # Saving with custom id: username
        db.child("users").child(request.user).set(data)
        return redirect('viewdetails')

def search_users(request):
    if request.method == "POST":
        users_list=[]
        searched =request.POST['searched']
        # 'Contains' search query
        users = db.child("users").get()
        for user in users.each():
            if searched in user.val()['vehicle_number_plate']:
                users_list.append(user.val())

        return render(request, 'accident/search_users.html',{'searched':searched, 'users_list':users_list})
    else:
        return render(request, 'accident/search_users.html')

# Emergency

def emergencydetail(request):
   
    if request.method == 'GET':
        return render(request, 'accident/emergencydetail.html')
    else:
        try:
            form_filled_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            file= request.FILES['img']
            file_format = file.name.split('.')[-1] 
            storage.child(f"accidents_image/{request.POST['accident-vehicle-number']+form_filled_date_time}.{file_format}").put(file)
            image_url=storage.child(f"accidents_image/{request.POST['accident-vehicle-number']+form_filled_date_time}.{file_format}").get_url(None)

            data = {
                "full_name":request.POST['full-name'],
                "mobile_no":request.POST['mobile-no'],
                "accident_vehicle_number":request.POST['accident-vehicle-number'],
                "accident_image_url":image_url,
                "location_link": request.POST['location-link'],
                "form_fill_date_time": form_filled_date_time
            }

            # Saving with custom id: username
            db.child("form_fillers").push(data)

            return render(request, 'accident/emergencydetail.html', {'msg':"You've successfully filled the form."})
        except:
            return render(request, 'accident/emergencydetail.html', {'msg':"The form couldn't be saved."})

def viewemergency(request):
    if request.user.is_superuser == True:
        accidents_list=[]
        accidents = db.child("form_fillers").order_by_child("form_fill_date_time").get()
        if accidents.val():
            for accident in accidents.each():
                accidents_list.append(accident.val())

        return render(request, 'accident/admin.html', {'accidents_list': accidents_list})

def search_emergency(request):
    if request.method == "POST":
        accidents_list=[]
        searched =request.POST['searched']
        # 'Contains' search query
        accidents = db.child("form_fillers").get()
        for accident in accidents.each():
            if searched in accident.val()['accident_vehicle_number']:
                accidents_list.append(accident.val())

        return render(request, 'accident/search_emergency.html',{'searched':searched, 'accidents_list':accidents_list})
    else:
        return render(request, 'accident/search_emergency.html')
    
def user_data(request, username):
    if request.user.is_superuser == True:
        user_details = db.child("users").order_by_child("username").equal_to(username).limit_to_first(1).get()
        if user_details.val():
            user_details=user_details.val()
            for k, v in user_details.items():
                user_details=v

        return render(request, 'accident/userdata.html', {'user_details':user_details})

# API
@api_view(['GET'])
def user_realtime_data(request, username):
    # Responding with the user details part which is being updated by the hardware
    user_details = db.child("users").order_by_child("username").equal_to(username).limit_to_first(1).get()
    if user_details.val():
        user_details=user_details.val()
        for k, v in user_details.items():
            user_details=v
    data = {
        "seatbelt_on":user_details['seatbelt_on'],
        "alcohol_detected":user_details['alcohol_detected'],
        "collision_detected":user_details['collision_detected'],
        "vib_sensor_on":user_details['vib_sensor_on'],
        "flame_detected":user_details['flame_detected'],
    }
    return JsonResponse(data)


