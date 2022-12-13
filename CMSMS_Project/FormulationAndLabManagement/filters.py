import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

class ProductsFilter(django_filters.FilterSet):
    product_name = CharFilter(field_name='product_name', lookup_expr='icontains', label="Product Name")
    product_category = CharFilter(field_name='product_category', label="Category", lookup_expr='icontains')

    class Meta:
        model = products
        fields = [
            'product_name',
            'product_category',
        ]


class EquipmentsFilter(django_filters.FilterSet):
    category = CharFilter(field_name='category', lookup_expr='icontains', label="Category")
    condition = CharFilter(field_name='condition', lookup_expr='icontains', label="Condition")

    class Meta:
        model = equipments
        fields = [
            'category',
            'condition',
        ]

class TestFilter(django_filters.FilterSet):
    test_name = CharFilter(field_name='test_name', lookup_expr='icontains', label="Test Name")
    product = CharFilter(field_name='product', lookup_expr='icontains', label="Product")

    class Meta:
        model = schedule_test
        fields = [
            'product',
            'test_name',
            'status',
        ]


class ChemicalFilter(django_filters.FilterSet):
    chemical_name = CharFilter(field_name='chemical_name', lookup_expr='icontains', label="Chemical Name")

    class Meta:
        model = test_chemicals
        fields = [
            'chemical_name',
            'status',
        ]