from django import forms
from django.forms import ModelForm, widgets
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class AddIncome(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'amount',
            'date',
        ]

        labels = {
            'amount': 'Amount',
            'date': 'Due Date',
        }

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        }


class AddExpenses(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = [
            'amount',
            'date',
            'type',
            'repetition_interval',
        ]

        labels = {
            'amount': 'Amount',
            'date': 'Due Date',
            'type': 'Type',
            'repetition_interval': 'Category',
        }

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Expense Type0'}),
            'repetition_interval': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Category'}),
        }

class AddProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = [
            'productName',
            'category',
            'target_quantity',
            'due_date',
            'status'
        ]

        labels = {
            'productName': 'Product Name',
            'category': 'Category',
            'target_quantity': 'Target Quantity',
            'due_date': 'Due Date',
            'status': 'Status',
        }

        widgets = {
            'productName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'In Days'}),
        }


class AddProductionCostForm(forms.ModelForm):
    class Meta:
        model = ProductionCost
        fields = [
            'Total_ProductCost',
            'date',
            'category',
            'description',
        ]

        labels = {
            'Total_ProductCost': 'Total Production Cost',
            'category': 'Category',
            'description': 'Description',
        }

        widgets = {
            'Total_ProductCost': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Production Cost'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddDirectMaterialCostForm(forms.ModelForm):
    class Meta:
        model = DirectMaterialCost
        fields = [
            'Total_DMAmount',
            'date',
            'category',
            'description',
        ]

        labels = {
            'category': 'Category',
            'description': 'Description',
            'Total_DMAmount': 'Total Direct Material Amount',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Total_DMAmount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Direct Material Cost'}),
        }


class AddDirectLaborCostForm(forms.ModelForm):
    class Meta:
        model = DirectLaborCost
        fields = [
            'Total_DLAmount',
            'date',
            'category',
            'description',
        ]

        labels = {
            'category': 'Category',
            'description': 'Description',
            'Total_DLAmount': 'Total Direct Labor Amount',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Total_DLAmount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Direct Labor Cost'}),
        }


class AddFactoryOverheadCostForm(forms.ModelForm):
    class Meta:
        model = FactoryOverheads
        fields = [
            'Total_FOAmount',
            'date',
            'category',
            'description',
        ]

        labels = {
            'category': 'Category',
            'description': 'Description',
            'Total_FOAmount': 'Total Factory OverHeads Amount',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Total_FOAmount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Factory Overheads Cost'}),
        }


class RetailPriceForm(forms.ModelForm):
    class Meta:
        model = RetailPrice
        fields = [
            'Total_RPAmount',
            'product_name',
            'description',

        ]

        labels = {
            'product_name': 'product name',
            'RPamount': 'Retail price',
            'Total_ProductCost': 'Total Production Cost',
            'markup_Price': 'Markup Price',
            'description': 'Description',
            'Total_RPAmount': 'Total Retail Price',
        }

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Total_RPAmount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Total Retail Price'}),
        }
