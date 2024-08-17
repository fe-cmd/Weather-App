import email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import json
import urllib.request
# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=ac184f978eb937289e97b5e258356cb0").read()
        json_data = json.loads(res)
        data = {
            "country_code":str(json_data['sys']['country']),
            "coordinate" :str(json_data['coord']['lon']) + ' ' +
            str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp'])+'k',
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
        }

    else:
        data = {}
        city = ''
    return render(request, 'index.html', {'city':city, 'data':data})

def register(request):
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already Exist')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Already Exist')
            return redirect('register')
        else:
         user = User.objects.create_user(username=username, email=email, password=password)
         user.save();
         return redirect('login')
    else:
        messages.info(request, 'Password does not correspond!!!')
        return redirect('register')

  else:      
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('intro')
        else:
            messages.info(request, 'Credentials Invalid!!!')
            return redirect('login')

    else:        
      return render(request, 'login.html')

def intro(request):
    if request.method == 'POST':
        return redirect('index')
    else:
     return render(request, 'intro.html')


def logout(request):
    auth.logout(request)
    return redirect('register')