from django.db import models
from WarehouseManagement.models import Product

PROGRESS = (
    ('', 'Select a Status'),
    ('Received', 'Received'),
    ('Preparing', 'Preparing'),
    ('Dispatched', 'Dispatched'),
    ('Delivered', 'Delivered'),
)


class Order(models.Model):
    orderID = models.CharField(max_length=7, null=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(null=False)
    receivedDate = models.DateField(auto_now_add=True)
    progress = models.CharField(max_length=30, null=True, choices=PROGRESS, default='Received')

    # def __str__(self):
    #     return f'{self.product.itemName} - {self.quantity} - {self.progress}'


class Driver(models.Model):
    License = (
        ('License Valid', 'License Valid'),
        ('License Expired', 'License Expired'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    fullname = models.CharField(max_length=100, null=True)
    contact_number = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=20, null=True, choices=GENDER)
    LicenseNumber = models.CharField(max_length=100, null=True)
    nic = models.CharField(max_length=100, null=True)
    LicenseValid = models.CharField(max_length=20, null=True, choices=License)

    def __str__(self):
        return self.fullname


class Vehicle(models.Model):
    condition = (
        ('Need to be repaired', 'Need to be repaired'),
        ('Good condition', 'Good condition'),
    )

    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    modelVehicle = models.CharField(max_length=20, null=True)
    brand = models.CharField(max_length=20, null=True)
    trim = models.CharField(max_length=20, null=True)
    LicensePlate = models.CharField(max_length=50, null=True)
    exteriorColor = models.CharField(max_length=20, null=True)
    year = models.PositiveIntegerField(null=True)
    engineCapacity = models.CharField(max_length=20, null=True)
    mileage = models.CharField(max_length=20, null=True)
    fuelType = models.CharField(max_length=20, null=True)
    quantity = models.PositiveIntegerField(null=True)
    condition = models.CharField(max_length=20, null=True, choices=condition)
    transmission = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.LicensePlate


class DeliveryCost(models.Model):
    PROVINCE = [
        ('Western Province', 'Western Province'),
        ('Southern Province', 'Southern Province'),
        ('Eastern Province', 'Eastern Province'),
        ('Central Province', 'Central Province'),
        ('Northcentral Province', 'Northcentral Province'),
        ('Northern Province', 'Northern Province'),
        ('Northwest Province', 'Northwest Province'),
        ('Uwa Province', 'Uwa Province'),
    ]

    province = models.CharField(max_length=200, null=True, choices=PROVINCE)
    delivery_cost = models.FloatField(null=True)
