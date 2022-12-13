import django_filters
from .models import *
from django_filters import NumberFilter
from django.forms.widgets import TextInput


class RawMaterialFilter(django_filters.FilterSet):
    quantity_less = NumberFilter(field_name="quantity", lookup_expr='lte',
                                 widget=TextInput(attrs={'placeholder': 'Quantity <='}))

    class Meta:
        model = RawMaterial
        fields = ('reorder_level', 'deficiency_request')


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = ('rawmaterial', 'status')


class BatchFilter(django_filters.FilterSet):
    class Meta:
        model = Batch
        fields = ('id', 'status')



