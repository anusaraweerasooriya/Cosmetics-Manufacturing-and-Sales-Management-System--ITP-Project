import django_filters
from .models import *


class IncomeFilter(django_filters.FilterSet):
    class Meta:
        model = Income
        fields = ('amount', 'date')


class ExpensesFilter(django_filters.FilterSet):
    class Meta:
        model = Expenses
        fields = ('amount', 'type', 'repetition_interval')


class ProductionCostFilter(django_filters.FilterSet):
    class Meta:
        model = ProductionCost
        fields = ('Total_ProductCost', 'category')


class DirectMaterialCostFilter(django_filters.FilterSet):
    class Meta:
        model = DirectMaterialCost
        fields = ('Total_DMAmount', 'category')


class DirectLaborCostFilter(django_filters.FilterSet):
    class Meta:
        model = DirectLaborCost
        fields = ('Total_DLAmount', 'category')


class FactoryOverheadsFilter(django_filters.FilterSet):
    class Meta:
        model = FactoryOverheads
        fields = ('Total_FOAmount', 'category')


class RetailPriceFilter(django_filters.FilterSet):
    class Meta:
        model = RetailPrice
        fields = ('Total_RPAmount',)
