from django import forms
from django.forms import ModelForm, widgets
from django.core.exceptions import ValidationError
from .models import *

class AddProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = [
            'product_name',
            'product_category',
            'description',
            'preparation_method',
            'duration',
            'product_image',
        ]

        labels = {
            'product_name': 'Product Name',
            'product_category': 'Category',
            'description': 'Description',
            'preparation_method': 'Method of Preparation',
            'duration': 'Duration',
            'product_image': 'Upload Image',
        }

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Name'}),
            'product_category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Product Category'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Description'}),
            'preparation_method': forms.Textarea(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'In Days'}),
        }

class AddEquipmentForm(forms.ModelForm):
    class Meta:
        model = equipments
        fields = '__all__'

        labels = {
            'equipment_id': 'Equipment ID',
            'Category': 'Category',
            'Condition': 'Condition',
        }

        widgets = {
            'equipment_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ID'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }

class UpdateEquipmentForm(forms.ModelForm):
    class Meta:
        model = equipments
        fields = '__all__'

        labels = {
            'equipment_id': 'Equipment ID',
            'Category': 'Category',
            'Condition': 'Condition',
        }

        widgets = {
            'equipment_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'category': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }


class AddChemicalForm(forms.ModelForm):
    class Meta:
        model = test_chemicals
        fields = '__all__'

        labels = {
            'chemical_name': 'Chemical Name',
            'available_quantity': 'Available Quantity',
            'status': 'Status',
        }

        widgets = {
            'chemical_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Chemical Name'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'In Grams'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class UpdateChemicalForm(forms.ModelForm):
    class Meta:
        model = test_chemicals
        fields = '__all__'

        labels = {
            'chemical_name': 'Chemical Name',
            'available_quantity': 'Available Quantity',
            'status': 'Status',
        }

        widgets = {
            'chemical_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'In Grams'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ScheduleTestForm(forms.ModelForm):
    class Meta:
        model = schedule_test
        fields = '__all__'

        labels = {
            'product': 'Product',
            'test_name': 'Test Name',
            'method': 'Method',
        }

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Product'}),
            'test_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Test Name'}),
            'method': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
