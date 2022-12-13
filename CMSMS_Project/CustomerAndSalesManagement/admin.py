from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(SalesProduct)
admin.site.register(Tag)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ProductReview)
admin.site.register(SalesTeam)
admin.site.register(SalesTeamMembers)
admin.site.register(SalesTask)
admin.site.register(BulkOrderRequest)
admin.site.register(BulkOrderItems)



