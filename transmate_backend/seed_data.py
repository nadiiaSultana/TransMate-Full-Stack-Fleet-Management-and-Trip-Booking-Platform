import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from apps.vehicles.models import VehicleType
for item in [
    {'name':'Bike','base_fare':'50.00','per_km_rate':'15.00','capacity':1,'description':'Fast and low-cost transport'},
    {'name':'Car','base_fare':'100.00','per_km_rate':'25.00','capacity':4,'description':'Standard private car service'},
    {'name':'Microbus','base_fare':'300.00','per_km_rate':'50.00','capacity':10,'description':'Family or group travel'},
    {'name':'Truck','base_fare':'500.00','per_km_rate':'80.00','capacity':2,'description':'Goods transportation service'},
]:
    VehicleType.objects.get_or_create(name=item['name'], defaults=item)
print('Seed vehicle types created.')
