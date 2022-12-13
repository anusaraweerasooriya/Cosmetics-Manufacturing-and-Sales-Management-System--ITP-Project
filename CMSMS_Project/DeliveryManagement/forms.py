from django.forms import ModelForm
from .models import *
from django import forms


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class OrderItemRequestForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


