import django_filters
from .models import *


class DriverFilter(django_filters.FilterSet):
    class Meta:
        model = Driver
        fields = '__all__'
        exclude = ['contact_number', 'email', 'nic', 'LicenseValid']


class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude = ['trim', 'exteriorColor', 'year', 'engineCapacity', 'mileage', 'fuelType', 'quantity', 'condition', 'transmission', 'driver']
