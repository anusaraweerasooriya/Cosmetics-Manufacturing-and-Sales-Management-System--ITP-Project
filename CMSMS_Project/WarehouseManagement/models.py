from django.db import models
from EmployeeManagement.models import Employees
from BatchProductionManagement.models import Batch


class Product(models.Model):
    product = models.ForeignKey(Batch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    reorderLevel = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.product.schedule_id.product_code.product_name}'


REQS = (
    ('', 'Select a One Option'),
    ('BP Manager', 'BP Manager'),
    ('Supplier Manager', 'Supplier Manager'),
)

REQ_STATUS = (
    ('', 'Select a Status'),
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Received', 'Received'),
)

TYPE = (
    ('', 'Select a Type'),
    ('Raw Material', 'Raw Material'),
    ('Equipment', 'Equipment'),
    ('Packaging', 'Packaging'),
    ('Product', 'Product'),
)


class WarehouseRequest(models.Model):
    request_ID = models.PositiveIntegerField(max_length=4, null=True)
    req_from = models.CharField(max_length=30, null=True, choices=REQS)
    type = models.CharField(max_length=20, null=True, choices=TYPE)
    itemName = models.CharField(max_length=30, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date = models.DateField(null=True, auto_now_add=True)
    due_Date = models.DateField(null=True)
    status = models.CharField(max_length=30, null=True, choices=REQ_STATUS, default='Pending')

    def __str__(self):
        return f'{self.itemName} - {self.type} - {self.quantity} - {self.req_from}'


class RawMaterial(models.Model):
    itemID = models.CharField(max_length=7, null=True)
    itemName = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True)
    description = models.TextField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    expireDate = models.DateField(null=True)
    receivedDate = models.DateField(null=True)

    def __str__(self):
        return f'{self.itemName} - {self.category} - {self.quantity}'


EQ_STATUS = (
    ('', 'Select a Status'),
    ('Fair', 'Fair'),
    ('Good', 'Good'),
    ('Excellent', 'Excellent'),
)

EQ_CATEGORIES = (
    ('', 'Select a Category'),
    ('Dock', 'Dock'),
    ('Conveyor', 'Conveyor'),
    ('Storage', 'Storage'),
    ('Lifting ', 'Lifting '),
    ('Packing', 'Packing'),
)


class Equipment(models.Model):
    itemID = models.CharField(max_length=7, null=True)
    itemName = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True, choices=EQ_CATEGORIES)
    description = models.TextField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=20, null=True, choices=EQ_STATUS)
    lastMaintenanceDate = models.DateField(null=True)
    nextMaintenanceDate = models.DateField(null=True)

    def __str__(self):
        return f'{self.itemName} - {self.category} - {self.quantity}'


PK_TYPES = (
    ('', 'Select a Type'),
    ('Plastic', 'Plastic'),
    ('Glass', 'Glass'),
    ('Steel', 'Steel'),
    ('Aluminum', 'Aluminum'),
    ('Paper and Paperboard', 'Paper and Paperboard'),
    ('Polythene', 'Polythene'),
)

PK_CATEGORIES = (
    ('', 'Select a Category'),
    ('Primary ', 'Primary '),
    ('Secondary', 'Secondary'),
    ('Tertiary ', 'Tertiary '),
)


class Packaging(models.Model):
    itemID = models.CharField(max_length=7, null=True)
    itemName = models.CharField(max_length=30, null=True)
    category = models.CharField(max_length=30, null=True, choices=PK_CATEGORIES)
    description = models.TextField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)
    reorderLevel = models.PositiveIntegerField(null=True)
    materialType = models.CharField(max_length=20, null=True, choices=PK_TYPES)

    def __str__(self):
        return f'{self.itemName} - {self.category} - {self.quantity}'


SECTORS = (
    ('', 'Select a Sector'),
    ('Loading Unloading', 'Loading Unloading'),
    ('Storage', 'Storage'),
    ('Order Preparation', 'Order Preparation'),
    ('Packing', 'Packing'),
    ('Dispatch and Outflow', 'Dispatch and Outflow'),
    ('Technical', 'Technical'),
)

AVAILABILITY = (
    ('', 'Select an Availability'),
    ('Free', 'Free'),
    ('On a Job', 'On a Job'),
)


class WarehouseEmployee(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)
    workingArea = models.CharField(max_length=20, null=True, choices=SECTORS)
    availability = models.CharField(max_length=10, null=True, choices=AVAILABILITY, default='Free')

    def __str__(self):
        return f'{self.employee.firstname}'


class History(models.Model):
    itemID = models.CharField(max_length=7, null=True)
    itemName = models.CharField(max_length=30, null=True)
    quantity = models.PositiveIntegerField(null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    action = models.CharField(max_length=20, null=True)
    affect_table = models.CharField(max_length=20, null=True)
