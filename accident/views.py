from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Accidentform
from .forms import EmergencyForm
from .models import Accident
from .models import Emergency
from django.contrib import messages
import pyrebase
from time import sleep



firebaseConfig = {
  'apiKey': "AIzaSyCAha5DfT2LigmUMI0fpKJmkxTbgBjpHgU",
  'authDomain': "accident-b00b3.firebaseapp.com",
  'databaseURL': "https://accident-b00b3-default-rtdb.asia-southeast1.firebasedatabase.app/",
  'projectId': "accident-b00b3",
  'storageBucket': "accident-b00b3.appspot.com",
  'messagingSenderId': "31977108867",
  'appId': "1:31977108867:web:788ea2a4548b71d6f2b2b6",
  'measurementId': "G-3X8XBRMG6M"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()



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
    if request.user.is_superuser == True:
        return render(request, 'accident/admin.html')
    else:
        if request.method == 'GET':
            return render(request, 'accident/userdetail.html', {'form': Accidentform})
        else: 
            accidents=Accident.objects.filter(user=request.user)
            if(accidents):
                msg = "You've already filled the form."
                return render(request, 'accident/viewdetails.html', {'msg': msg})
            else:
                form = Accidentform(request.POST, request.FILES)
                data = request.POST
                db.child(data['user_name']).set(data)
                new = form.save(commit=False)
                new.user = request.user
                new.save()
                return redirect('viewdetails')
            
def viewdetails(request):
    if request.user.is_superuser == True:
        accidents=Accident.objects.all()
        # db.child("users").get()
        return render(request, 'accident/adminuser.html', {'accidents': accidents})
    else:
        accidents = Accident.objects.filter(user=request.user)
        # accident = accidents[0]
        # # print(accident)
        # # accident = dict(accident)
        # accidents = db.child(accident).get().val()
        # print(accident)
        return render(request, 'accident/viewdetails.html', {'accidents': accidents})

def deletedetails(request):
    accident = get_object_or_404(Accident, user=request.user)
    if request.method == 'POST':
        accident.delete()
        msgs = "Your details have been successfully deleted!"
        return render(request, 'accident/viewdetails.html', {'msgs': msgs})

def editdetails(request):
    accident = get_object_or_404(Accident, user=request.user)
    if request.method == 'GET':
        context = {'form': Accidentform(instance=accident)}
        return render(request,'accident/editdetails.html',context)
    elif request.method == 'POST':
        form = Accidentform(request.POST,files=request.FILES, instance=accident)
        if form.is_valid():
            # form = Accidentform(request.POST, request.FILES)
            data = request.POST
            db.child(data['user_name']).set(data)
            form.save()
            return redirect('viewdetails')
        else:
            return render(request,'accident/editdetails.html',{'form':form})

def search_users(request):
    if request.method == "POST":
        searched =request.POST['searched']
        users = Accident.objects.filter(vehicle_number_plate__contains= searched)

        return render(request, 'accident/search_users.html',{'searched':searched, 'users':users})
    else:
        return render(request, 'accident/search_users.html',{})

def search_emergency(request):
    if request.method == "POST":
        searched =request.POST['searched']
        users = Emergency.objects.filter(accident_vehicle_number__contains= searched)

        return render(request, 'accident/search_emergency.html',{'searched':searched, 'users':users})
    else:
        return render(request, 'accident/search_emergency.html',{})

def emergencydetail(request):
    if request.user.is_superuser == True:
        return redirect('viewemergency')
    else:
        if request.method == 'GET':
            return render(request, 'accident/emergencydetail.html', {'form': EmergencyForm})
        else:
            try:
                form = EmergencyForm(request.POST, request.FILES)
                new = form.save(commit=False)
                new.user = request.user
                new.save()

                msg = "You've successfully filled the form."
                return render(request, 'accident/emergencydetail.html', {'form':EmergencyForm, 'msg':msg})
            except:
                return render(request, 'accident/emergencydetail.html', {'form':EmergencyForm, 'error':'Bad data passed in. Try again.'})

def viewemergency(request):
    if request.user.is_superuser == True:
        accidents= Emergency.objects.all()
        return render(request, 'accident/admin.html', {'accidents': accidents})
    else:
        accidents = Emergency.objects.all()
        return render(request, 'accident/viewemergency.html', {'accidents': accidents})




