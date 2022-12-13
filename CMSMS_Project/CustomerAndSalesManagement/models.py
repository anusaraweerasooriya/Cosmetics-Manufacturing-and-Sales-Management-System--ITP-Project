from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from EmployeeManagement.models import *
from CostAnalysisManagement.models import RetailPrice


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class SalesProduct(models.Model):
    CATEGORY = [
        ('', 'Select a category..'),
        ('S', 'Skin Cosmetics'),
        ('F', 'Face Makeup'),
        ('N', 'Nail Cosmetics'),
        ('H', 'Hair Cosmetics'),
        ('O', 'Other Categories'),
    ]
    # product = models.ForeignKey(RetailPrice, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    selling_price = models.FloatField(null=True)
    production_price = models.FloatField(null=True, blank=True)
    retail_price = models.FloatField(null=True)
    # production_price = models.OneToOneField(RetailPrice, null=True, on_delete=models.CASCADE)
    # retail_price = models.OneToOneField(RetailPrice, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    product_image = models.ImageField(default="", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, )
    tags = models.ManyToManyField(Tag, null=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.product_image
        except:
            url = '/static/images/product_logo.jpeg'
        return url

    @property
    def calculate_discount(self):
        discount = (self.retail_price - self.selling_price) * 100 / self.retail_price
        return discount

    @property
    def get_vote_count(self):
        reviews = self.productreview_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        ratio = (up_votes / total_votes) * 100

        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

    @property
    def get_reviewers(self):
        customers = self.productreview_set.all().values_list('customer__id', flat=True)
        return customers


class Customer(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)  # unique=True
    mobile_number = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDER)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def image_url(self):
        try:
            url = self.profile_picture.url
        except:
            url = '/static/images/avatar.png'
        return url


class Order(models.Model):
    ORDER_STATUS = [
        ('Order confirmed', 'Order confirmed'),
        ('Packaging up the order', 'Packaging up the order'),
        ('Order shipped', 'Order shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=False, default=timezone.datetime.now())
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    order_status = models.CharField(max_length=50, null=True, blank=True, choices=ORDER_STATUS, default='Order '
                                                                                                'confirmed')
    net_total = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total_price for item in order_items])
        self.net_total = total
        self.save()
        return total

    @property
    def get_cart_discount(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total_discount for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(SalesProduct, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total = self.product.selling_price * self.quantity
        return total

    @property
    def get_total_discount(self):
        discount = (self.product.retail_price * self.quantity) - (self.product.selling_price * self.quantity)
        return discount


class ShippingAddress(models.Model):
    PROVINCE = [
        ('', 'Select a Province'),
        ('Western Province', 'Western Province'),
        ('Southern Province', 'Southern Province'),
        ('Eastern Province', 'Eastern Province'),
        ('Central Province', 'Central Province'),
        ('Northcentral Province', 'Northcentral Province'),
        ('Northern Province', 'Northern Province'),
        ('Northwest Province', 'Northwest Province'),
        ('Uwa Province', 'Uwa Province'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(SalesProduct, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True, choices=PROVINCE)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class ProductReview(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(SalesProduct, on_delete=models.CASCADE)
    text_review = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['customer', 'product']]

    def __str__(self):
        return self.value


class BulkOrderRequest(models.Model):
    PROVINCE = [
        ('', 'Select a Province'),
        ('Western Province', 'Western Province'),
        ('Southern Province', 'Southern Province'),
        ('Eastern Province', 'Eastern Province'),
        ('Central Province', 'Central Province'),
        ('Northcentral Province', 'Northcentral Province'),
        ('Northern Province', 'Northern Province'),
        ('Northwest Province', 'Northwest Province'),
        ('Uwa Province', 'Uwa Province'),
    ]

    ORDER_STATUS = [
        ('Request Pending', 'Request Pending'),
        ('Order Accepted', 'Order Accepted'),
        ('Request Cancelled', 'Order Cancelled')
    ]

    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=False)
    company_name = models.CharField(max_length=200)
    mobile_number = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    street_address = models.CharField(max_length=200, null=True, blank=False)
    city = models.CharField(max_length=200, null=True, blank=False)
    province = models.CharField(max_length=200, null=True, blank=False, choices=PROVINCE)
    zip_code = models.IntegerField(null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(max_length=20, default='Request Pending')


class BulkOrderItems(models.Model):
    bulk_order = models.ForeignKey(BulkOrderRequest, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(SalesProduct, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class SalesTeam(models.Model):
    team_name = models.CharField(max_length=200, null=True)
    team_description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    no_of_employees = models.IntegerField(default=2, null=True)

    def __str__(self):
        return str(self.team_name)


class SalesTeamMembers(models.Model):
    team_member = models.OneToOneField(Employees, null=True, on_delete=models.DO_NOTHING, blank=True)
    sales_team = models.ForeignKey(SalesTeam, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team_member)

    @property
    def assign_members(self):
        employees = Employees.objects.filter(department_id='Sales Department')
        self.team_member = employees


class SalesTask(models.Model):
    TASK_STATUS = [
        ('Assigned', 'Assigned'),
        ('Status Pending', 'Task Pending'),
        ('Task Completed', 'Task Completed'),
    ]

    task_name = models.CharField(max_length=200, null=True)
    task_description = models.CharField(max_length=200, null=True)
    sales_team = models.OneToOneField(SalesTeam, on_delete=models.CASCADE, null=True)
    progress = models.IntegerField(default=0, null=True, blank=True)
    task_status = models.CharField(max_length=20, null=True, choices=TASK_STATUS, default='Assigned')

    def __str__(self):
        return str(self.task_name)
