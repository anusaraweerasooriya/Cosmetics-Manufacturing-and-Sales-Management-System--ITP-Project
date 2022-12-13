from django.db import models
from django.utils import timezone

DEPARTMENTS = (
    ('Warehouse', 'Warehouse'),
    ('Batch Production', 'Batch Production'),
    ('Delivery Management', 'Delivery Management'),
    ('Laboratory', 'Laboratory'),
    ('Sales', 'Sales'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

STATUS = (
    ('Accepted', 'Accepted'),
    ('Pending', 'Pending'),
)


################# Department #####################

class Department(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


################# Position #####################

class Position(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


################# Attendance #####################

class Attendance(models.Model):
    eid = models.TextField()
    date = models.DateField()
    time = models.TimeField()


    def __str__(self):
        return self.eid

################# Leave #####################

class Leave(models.Model):
    eid = models.TextField()
    type = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.TextField()

    def __str__(self):
        return self.eid


################# Employee #####################

class Employees(models.Model):
    code = models.CharField(max_length=100, blank=True)
    firstname = models.TextField()
    middlename = models.TextField(blank=True, null=True)
    lastname = models.TextField()
    gender = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contact = models.TextField()
    address = models.TextField()
    email = models.TextField()
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_hired = models.DateField()
    salary = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, null=True, default="Pending")
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname + ' ' + self.middlename + ' ' + self.lastname + ' '
