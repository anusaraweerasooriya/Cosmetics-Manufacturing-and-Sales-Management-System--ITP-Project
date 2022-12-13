from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from django.utils.timezone import now


# Create your models here.


class Production(models.Model):
    CATEGORY = (
        ('Skin Cosmetics', 'Skin Cosmetics'),
        ('Hair Cosmetics', 'Hair Cosmetics'),
        ('Nail Cosmetics', 'Nail Cosmetics'),
        ('Face Makeup', 'Face Makeup')
    )

    productName = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    target_quantity = models.PositiveIntegerField(null=True)
    due_date = models.DateField(null=True)
    status = models.CharField(max_length=200, default='Scheduled', null=True)
    count = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.productName}'


class Income(models.Model):
    class ITypes(models.IntegerChoices):
        SAL = 1, "SALARY"
        BON = 2, "BONUS"
        GIF = 3, "GIFT"
        OTH = 4, "OTHER"

    class RInterval(models.IntegerChoices):
        NA = 1, 'N/A'
        DAY = 2, 'DAYS'
        WEK = 3, 'WEEKS'
        MON = 4, 'MONTHS'
        YEA = 5, 'YEARS'

    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Income {self.id}'


class Expenses(models.Model):
    class EType(models.IntegerChoices):
        REN = 1, "RENT"
        BIL = 2, "BILLS"
        TRA = 3, "TRAVEL"
        MET = 4, "MATERIALS"

    class RInterval(models.IntegerChoices):
        DAY = 1, "DAYS"
        WEK = 2, "WEEKS"
        MON = 3, "MONTHS"
        YER = 4, "YEAR"

    amount = models.FloatField(default=0)
    date = models.DateTimeField(null=True)
    type = models.PositiveIntegerField(choices=EType.choices)
    repetitive = models.BooleanField(default=False)
    repetition_interval = models.PositiveIntegerField(choices=RInterval.choices, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Expenses {self.id} - {self.type} '


class Profit(models.Model):
    class PType(models.IntegerChoices):
        MON = 1, "MONTHLY"
        ANU = 2, "ANNUALLY"

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveIntegerField(choices=PType.choices)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profit {self.id} - {self.type}'


class ProductionCost(models.Model):
    CATEGORY = (
        ('Skin Cosmetics', 'Skin Cosmetics'),
        ('Hair Cosmetics', 'Hair Cosmetics'),
        ('Nail Cosmetics', 'Nail Cosmetics'),
        ('Face Makeup', 'Face Makeup'),
    )
    amount = models.FloatField(default=0)
    date = models.DateTimeField(null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    created_at = models.DateTimeField(auto_now_add=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    Total_DMAmount = models.FloatField(default=0)
    Total_DLAmount = models.FloatField(default=0)
    Total_FOAmount = models.FloatField(default=0)
    Total_ProductCost = models.FloatField(default=0)

    def __str__(self):
        return f'Expenses {self.Total_ProductCost} - {self.category} - {self.description} '


class DirectMaterialCost(models.Model):
    CATEGORY = (
        ('Skin Cosmetics', 'Skin Cosmetics'),
        ('Hair Cosmetics', 'Hair Cosmetics'),
        ('Nail Cosmetics', 'Nail Cosmetics'),
        ('Face Makeup', 'Face Makeup'),
    )

    DMamount = models.FloatField(default=0)
    date = models.DateTimeField(null=True)
    category = models.CharField(max_length=30, null=True, choices=CATEGORY)
    quantity = models.PositiveIntegerField(null=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    Total_DMAmount = models.FloatField(default=0)

    def __str__(self):
        return f' {self.id} - {self.category} - {self.quantity} - {self.description}'


class DirectLaborCost(models.Model):
    CATEGORY = (
        ('Wages', 'Wages'),
        ('Payroll Taxes', 'Payroll Taxes'),
        ('Workers Compensation', 'Workers Compensation'),
        ('Life Insurance', 'Life Insurance'),
        ('Health Insurance', 'Health Insurance'),
    )

    DLamount = models.FloatField(default=0)
    date = models.DateTimeField(null=True)
    category = models.CharField(max_length=30, null=True, choices=CATEGORY)
    quantity = models.PositiveIntegerField(null=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    Total_DLAmount = models.FloatField(default=0)

    def __str__(self):
        return f' {self.id} - {self.category} - {self.quantity} - {self.description}'


class FactoryOverheads(models.Model):
    CATEGORY = (
        ('Labor Hours required', 'Labor Hours required'),
        ('Labor Cost per hour', 'Labor Cost per hour'),
        ('Electricity Units', 'Electricity Units'),
        ('Rent of Factory Premises', 'Rent of Factory Premises'),
        ('Insurance Expenses', 'Insurance Expenses'),
        ('Depreciation of Machinery', 'Depreciation of Machinery'),
        ('Direct Cost of Machinery Oil', 'Direct Cost of Machinery Oil'),
        ('Electricity Cost Per Unit', 'Electricity Cost Per Unit'),
    )
    FOamount = models.FloatField(default=0)
    date = models.DateTimeField(null=True)
    category = models.CharField(max_length=30, null=True, choices=CATEGORY)
    quantity = models.PositiveIntegerField(null=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    Total_FOAmount = models.FloatField(default=0)

    def __str__(self):
        return f' {self.id} - {self.category} - {self.quantity}'


class RetailPrice(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    RPamount = models.FloatField(null=True)
    Total_ProductCost = models.FloatField(null=True)
    markup_Price = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    Total_RPAmount = models.FloatField(null=True)

    def __str__(self):
        return f' {self.product_name} '


class cost(models.Model):
    product_name = models.ForeignKey(RetailPrice, null=True, on_delete=models.SET_NULL)
    materials = models.CharField(max_length=1000, null=True)
    cost_qty = models.IntegerField(null=True)

    def __str__(self):
        return f' {self.materials.product_name}'
