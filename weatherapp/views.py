
from django.shortcuts import get_object_or_404, redirect, render
from decouple import config
import requests
from pprint import pprint 
from django.contrib import messages
from .models import City


def home(request):
   API_Key = config("API_KEY")
   user_city = request.GET.get('city')
   
   if user_city:
      url=f"https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API_Key}&units=metric"
      response=requests.get(url)
      if response.ok:
         content = response.json()
         res_city = content['name']
         if City.objects.filter(name=res_city):
            messages.warning(request,"City already exist!")
         else:
            City.objects.create(name=res_city)
            messages.success(request, "City created succesfully!")
      else:
         messages.error(request,"There is no city")
   
      return redirect("home")
   
   
   city_data = []
   cities = City.objects.all()
   
   for city in cities:
      url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Key}&units=metric"
      response=requests.get(url)
      content = response.json()
      data = {
      # 'city':content['name'],
      'city':city,
      'temp':content['main']['temp'],
      'icon':content['weather'][0]['icon'],
      'desc':content['weather'][0]['description'],
      'country' : content['sys']['country']
      }
      
      city_data.append(data)
      # pprint(city_data)
   
   context = {
      'city_data':city_data
   }
   
   
   # return render(request, "weatherapp/home.html", context)
   return render(request, "weatherapp/base.html", context)



def delete_city(request, id):
   city = get_object_or_404(City, id=id)
   city.delete()
   messages.success(request, "City has been deleted!")
   return redirect("home")