from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CityForm
from .models import City
import requests
# Create your views here.
def get_cur_weather():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url).json()
	# j = json.loads(r.text)
	lat = r['latitude']
	lon = r['longitude']
	city = r['region_name']
	cur_url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=0a2fad4d1a793d6c2d3cec6944844da2'
	r = requests.get(cur_url.format(lat,lon)).json()
	city_weather = {
			'temperature':r['main']['temp'],
			'description':r['weather'][0]['description'],
			'icon':r['weather'][0]['icon'],
			'city':city,
		}
	print(r)
	return city_weather

def index(request):
	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('index')
	else:
		form = CityForm()
	cur_weather = get_cur_weather()
	
	url 	= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0a2fad4d1a793d6c2d3cec6944844da2'
	weather_data = []
	cities = City.objects.all()
	# r = requests.get(url.format("tokyo"))
	# print(r.text)
	for city in cities:
		r = requests.get(url.format(city.city)).json()
		if r['cod']==200:
			temperature = r['main']['temp']
			description = r['weather'][0]['description']
			icon = r['weather'][0]['icon']
			city_weather = {
				'temperature':temperature,
				'description':description,
				'icon':icon,
				'city':city.city,
				'id':city.id,
			}
			weather_data.append(city_weather)
		else :
			messages.warning(request, city.city + ' is not a valid city')
			items = City.objects.filter(city = city.city)
			for item in items:
				item.delete()

	return render(request , 'weather.html' , {'weather_data':weather_data , 'cur_weather': cur_weather})

def delete(request , city_id):
	item = City.objects.get(pk=city_id)
	item.delete()
	return redirect('index')