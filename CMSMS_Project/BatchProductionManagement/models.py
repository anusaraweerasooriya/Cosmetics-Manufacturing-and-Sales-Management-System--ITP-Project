from django.db import models
import datetime
from FormulationAndLabManagement.models import products, formulation


class RawMaterial(models.Model):
    name = models.CharField(max_length=200, null=True)
    quantity = models.FloatField(null=True)
    reorder_level = models.FloatField(null=True)
    deficiency_request = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Request(models.Model):
    STATUS = (
        ('', 'Select Status'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Received', 'Received'),
    )
    rawmaterial = models.ForeignKey(RawMaterial, null=True, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(null=True)
    description = models.TextField(blank=True, null=True)
    date_requested = models.DateField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=200, default='Pending', null=True, choices=STATUS)

    def __str__(self):
        return f'{self.rawmaterial} - {self.quantity}'


class ScheduleProduction(models.Model):
    NET_WEIGHT = (
        ('', 'Select weight in ml/g'),
        (15, 15),
        (100, 125),
        (125, 125),
        (250, 250),
    )
    STATUS = (
        ('', 'Select Status'),
        ('Scheduled', 'Scheduled'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed')
    )
    product_code = models.ForeignKey(products, null=True, on_delete=models.DO_NOTHING)
    target_quantity = models.PositiveIntegerField(null=True)
    net_weight = models.PositiveIntegerField(null=True, choices=NET_WEIGHT)
    due_date = models.DateField(null=True)
    status = models.CharField(max_length=200, default='Scheduled', null=True, choices=STATUS)

    def __str__(self):
        return f'{self.product_code} - {self.status}'


class Batch(models.Model):
    STATUS = (
        ('', 'Select Status'),
        ('Ready', 'Ready'),
        ('Dispatched', 'Dispatched'),
        ('Received', 'Received'),
    )
    schedule_id = models.ForeignKey(ScheduleProduction, null=True, on_delete=models.DO_NOTHING)
    batch_quantity = models.PositiveIntegerField(null=True)
    manufacture_date = models.DateField(null=True)
    expiry_date = models.DateField(blank=True, null=True)
    batch_details = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=200, default='Ready', null=True, choices=STATUS)

    def __str__(self):
        return f'{self.schedule_id.product_code}'


class Machine(models.Model):
    CONDITION = (
        ('', 'Select Condition'),
        ('Brand New', 'Brand New'),
        ('Need Repair', 'Need Repair'),
        ('Under maintenance', 'Under maintenance'),
        ('Not Functional', 'Not Functional'),
    )
    item_name = models.CharField(max_length=200, null=True)
    model = models.CharField(max_length=200, null=True)
    year = models.PositiveIntegerField(null=True)
    description = models.TextField(blank=True, null=True)
    power_consumption = models.FloatField(null=True)
    net_weight = models.FloatField(null=True)
    dimensions = models.CharField(max_length=200, null=True)
    date_purchased = models.DateField(null=True)
    repair_duration = models.PositiveIntegerField(null=True)
    last_repair = models.DateField(null=True, blank=True)
    next_repair = models.DateField(null=True, blank=True)
    condition = models.CharField(max_length=200, default='Brand New', null=True, choices=CONDITION)
    image = models.ImageField(null=True, blank=True, upload_to="batch/", default="default_image.jpg")

    def __str__(self):
        return f'{self.item_name}'

    @property
    def image_url(self):
        try:
            url = self.image
        except:
            url = ''
        return url

    @property
    def calcNextRepair(self):
        next_repair = self.date_purchased + datetime.timedelta(days=self.repair_duration)
        return next_repair

    @property
    def calcLastRepair(self):
        last_repair = self.date_purchased
        return last_repair


class RawMaterialHistory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    reorder_level = models.FloatField(null=True, blank=True)
    last_updated = models.DateField(auto_now_add=True, null=True)
    action = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class RequestHistory(models.Model):
    STATUS = (
        ('', 'Select Status'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Received', 'Received'),
    )
    rawmaterial = models.ForeignKey(RawMaterial, null=True, blank=True, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_requested = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=200, default='Pending', null=True, blank=True, choices=STATUS)
    lastUpdated = models.DateField(auto_now_add=True, null=True)
    action = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.rawmaterial} - {self.quantity}'
