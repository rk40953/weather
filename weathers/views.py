import requests
from django.shortcuts import render , redirect
from .models import City
from .forms import CityForm

def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=13ca759c233d9fe9780a3cd55ddeb392'
    err_msg=''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                form.save()
            else:
                err_msg='city already exists in database'

    form = CityForm()

    cities = City.objects.all()


    weather_data=[]

    for city in cities:
        r=requests.get(url.format(city)).json()
        city_weather={
            'city': city.name,
            'temperature':r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'wind_speed': r['wind']['speed'],
            }
        weather_data.append(city_weather)

    context={
        'weather_data': weather_data , 'form': form
    }



    return render(request,'weathers/index.html',context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
