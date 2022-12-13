from django.forms import ModelForm
from .models import *
from django import forms


class RawMaterialForm(ModelForm):
    class Meta:
        model = RawMaterial
        fields = [
            'name',
            'quantity',
            'reorder_level',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = [
            'rawmaterial',
            'quantity',
            'description',
        ]

        widgets = {
            'rawmaterial': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ScheduleForm(ModelForm):
    class Meta:
        model = ScheduleProduction
        fields = [
            'product_code',
            'target_quantity',
            'net_weight',
            'due_date',
        ]

        widgets = {
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'target_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_weight': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'date'}),
        }


class UpdateScheduleForm(ModelForm):
    class Meta:
        model = ScheduleProduction
        fields = [
            'product_code',
            'target_quantity',
            'net_weight',
            'due_date',
        ]

        widgets = {
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'target_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_weight': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'date'}),
            # id = date necessary for date picking function
        }


class MachineryForm(ModelForm):
    class Meta:
        model = Machine
        fields = [
            'item_name',
            'model',
            'year',
            'description',
            'power_consumption',
            'net_weight',
            'dimensions',
            'date_purchased',
            'repair_duration',
            'image',
        ]

        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'power_consumption': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Length x Width x Height (mm)'}),
            'date_purchased': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'date'}),
            'repair_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'In Days'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
