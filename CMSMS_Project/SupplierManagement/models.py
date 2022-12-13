from django.db import models
from django.contrib.auth.models import User

Newsupplier_status = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
)


class Newsupplier(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=50, null=True)
    contact_no = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    product_category = models.CharField(max_length=20,
                 choices=[('Raw materials', 'Raw materials'), ('Packaging materials', 'Packaging materials'),
                          ('Equipments', 'Equipments')])
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=30, null=True, choices=Newsupplier_status, default='Pending')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.product_category}'


class SupplierInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=70, null=True)
    contact_no = models.CharField(max_length=20, null=True)
    product_category = models.CharField(
        max_length=20,
        choices=[('Raw materials', 'Raw materials'), ('Packaging materials', 'Packaging materials'),
                 ('Equipments', 'Equipments')]
    )
    profile_image = models.ImageField(default='avatar.png', upload_to='Profile_images')
    account_no = models.PositiveIntegerField(null=True, blank=True)
    bankWithBranch = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


order_status = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
    ('Re-ordered', 'Re-ordered'),
    ('Canceled', 'Canceled'),
    ('Paid', 'paid'),
    ('ordered', 'ordered'),
    ('toreturn', 'toreturn'),
)


class OrderRequest(models.Model):
    request_ID = models.PositiveIntegerField(null=True)
    itemName = models.CharField(max_length=20, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now_add=True)
    due_Date = models.DateField(null=True)
    SupplierID = models.ForeignKey(SupplierInfo, models.CASCADE, null=True)
    Note = models.TextField(max_length=100, null=True)
    status = models.CharField(max_length=30, null=True, choices=order_status, default='Pending')

    def __str__(self):
        return f'{self.request_ID}'


class SupplierProduct(models.Model):
    Product = models.CharField(max_length=50, null=True)
    Supplier = models.ForeignKey(User, models.CASCADE, null=True)
    Unit_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Unit = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f'{self.id} - {self.Product} sell by {self.Supplier} - {self.Unit_Price} per {self.Unit}'


class Invoice(models.Model):
    request_ID = models.OneToOneField(OrderRequest, on_delete=models.CASCADE, null=True)
    invoice_pdf = models.FileField(upload_to='invoices/pdfs/', null=True, blank=True)
    invoice_image = models.ImageField(upload_to='invoices/images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.id} - {self.request_ID}'


view_status = (
    ('viewed', 'viewed'),
    ('new', 'new'),
    ('received', 'received'),
)


class Order(models.Model):
    request_ID = models.OneToOneField(OrderRequest, on_delete=models.CASCADE, null=True)
    payment_image = models.ImageField(upload_to='s_orders/payslips/', null=True)
    orderedDate = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=100, null=True)
    further_details = models.TextField(null=True, blank=True)
    viewed_status = models.CharField(max_length=30, null=True, choices=view_status, default='new')

    def __str__(self):
        return f'{self.id}'


return_status = (
    ('pending', 'pending'),
    ('refunded', 'refunded'),
    ('re-shipped', 're-shipped'),
)


class Returns(models.Model):
    request_ID = models.OneToOneField(OrderRequest, on_delete=models.CASCADE, null=True)
    refund = models.BooleanField("Refund", default=False)
    Ship_again = models.BooleanField("Ship again", default=False)
    Description = models.TextField(null=True, blank=True)
    return_status = models.CharField(max_length=30, null=True, choices=return_status, default='pending')

    def __str__(self):
        return f'{self.id}-{self.request_ID}'




