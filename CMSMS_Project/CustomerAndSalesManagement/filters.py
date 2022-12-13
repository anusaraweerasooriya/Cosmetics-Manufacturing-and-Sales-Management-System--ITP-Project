import django_filters
from django_filters import *
from django.forms.widgets import *
from .models import *
from django import forms


class SalesProductsFilter(django_filters.FilterSet):
    max_price = NumberFilter(field_name='selling_price', lookup_expr='lte')
    min_price = NumberFilter(field_name='selling_price', lookup_expr='gte')

    class Meta:
        model = SalesProduct
        fields = ['category', 'vote_ratio']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
