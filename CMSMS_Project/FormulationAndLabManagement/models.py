from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class products(models.Model):
    CATEGORY = (
        ('Select Category', 'Select Category'),
        ('Skin Cosmetics', 'Skin Cosmetics'),
        ('Hair Cosmetics', 'Hair Cosmetics'),
        ('Nail Cosmetics', 'Nail Cosmetics'),
        ('Face Makeup', 'Face Makeup')
    )
    product_name = models.CharField(max_length=100, null=True, unique=True)
    product_category = models.CharField(max_length=100, null=True, choices=CATEGORY, default="Select Category")
    description = models.CharField(max_length=1000, null=True)
    preparation_method = models.TextField()
    duration = models.DurationField(null=True)
    product_image = models.ImageField(null=True, blank=True, upload_to="formulation/", default="default_image.jpg")

    def __str__(self):
        return self.product_name

class products_history(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_category = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    preparation_method = models.TextField()
    duration = models.DurationField(null=True)
    product_image = models.ImageField(null=True, blank=True, upload_to="formulation/", default="default_image.jpg")
    action = models.CharField(max_length=20, null=True)
    date = models.DateField(auto_now_add=True, null=True)


class formulation(models.Model):
    def quantitity_validate(value):
        if (value < 0):
            raise ValidationError(str(value) + " is not valid. Please enter valid quantity")

    product_name = models.ForeignKey(products, null=True, on_delete=models.SET_NULL)
    raw_material = models.CharField(max_length=1000, null=True)
    formulation_qty = models.FloatField(null=True, validators=[quantitity_validate])

    def __str__(self):
        return self.raw_material


class formulationhistory(models.Model):
    product_name = models.ForeignKey(products, null=True, on_delete=models.SET_NULL)
    raw_material = models.CharField(max_length=1000, null=True)
    formulation_qty = models.IntegerField(null=True)
    action = models.CharField(max_length=20, null=True)
    date = models.DateField(auto_now_add=True, null=True)


class lab_test(models.Model):
    product = models.ForeignKey(products, null=True, on_delete=models.SET_NULL)
    test_date = models.DateField(null=True)
    test_result = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.product.product_name

class harmfull_chemicals(models.Model):
    chemical_name = models.CharField(max_length=200, null=True)
    harmful_percentage = models.FloatField(null=True)

    def __str__(self):
        return self.chemical_name

class updated_products(models.Model):
    CATEGORY = (
        ('Skin Cosmetics', 'Skin Cosmetics'),
        ('Hair Cosmetics', 'Hair Cosmetics'),
        ('Nail Cosmetics', 'Nail Cosmetics'),
        ('Face Makeup', 'Face Makeup')
    )

    def duaration_validate(value):
        if (value < 31):
            raise ValidationError(str(value) + " duration is not sufficient")

    product_name = models.ForeignKey(products, null=True, on_delete=models.SET_NULL)
    product_category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.CharField(max_length=1000, null=True)
    preparation_method = models.CharField(max_length=5000, null=True)
    duration = models.DurationField(null=True, validators=[duaration_validate])
    isSafe = models.CharField(max_length=100, null=True)


class equipments(models.Model):
    CATEGORY = (
        ('Select Category', 'Select Category'),
        ('Test Tube', 'Test Tube'),
        ('Flask', 'Flask'),
        ('Beaker', 'Beaker'),
        ('Pipette', 'Pipette'),
        ('Burette', 'Burette'),
        ('Measuring Cylinder', 'Measuring Cylinder'),
        ('Laboratory Stand', 'Laboratory Stand'),
        ('Funnel', 'Funnel'),
    )

    CONDITION = (
        ('Choose Condition', 'Choose Condition'),
        ('Brand New', 'Brand New'),
        ('Used', 'Used'),
        ('Need Repair', 'Need Repair'),
    )

    equipment_id = models.CharField(max_length=50, null=True, unique=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY, default="Select Category")
    condition = models.CharField(max_length=100, null=True, choices=CONDITION, default='Choose Condition')

    def __str__(self):
        return self.equipment_id

class test_chemicals(models.Model):
    STATUS = (
        ('Select Status', 'Select Status'),
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    )

    def quantitity_validate(value):
        if (value < 0):
            raise ValidationError(str(value) + " is not valid. Please enter valid quantity")

    chemical_name = models.CharField(max_length=200, null=True, unique=True)
    available_quantity = models.FloatField(null=True, validators=[quantitity_validate])
    status = models.CharField(max_length=100, null=True, choices=STATUS, default="Select Status")

    def __str__(self):
        return self.chemical_name



class schedule_test(models.Model):
    STATUS = (
        ('Select Status', 'Select Status'),
        ('Success', 'Success'),
        ('Unsuccess', 'Unsucsess'),
        ('Pending', 'Pending'),
    )
    product = models.ForeignKey(products, null=True, on_delete=models.SET_NULL)
    test_name = models.CharField(max_length=200, null=True, unique=True)
    method = models.CharField(max_length=5000, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS, default="Select Status")

    def __str__(self):
        return self.test_name

class schedule_test_chemicals(models.Model):
    def quantitity_validate(value):
        if (value < 0):
            raise ValidationError(str(value) + " is not valid. Please enter valid quantity")

    test = models.ForeignKey(schedule_test, null=True, on_delete=models.SET_NULL)
    chemical = models.ForeignKey(test_chemicals, null=True, on_delete=models.SET_NULL)
    quantity = models.FloatField(null=True, validators=[quantitity_validate])




