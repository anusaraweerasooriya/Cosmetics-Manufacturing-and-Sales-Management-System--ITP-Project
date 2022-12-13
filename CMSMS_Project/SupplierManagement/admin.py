from django.contrib import admin
from .models import Newsupplier, SupplierProduct, OrderRequest, SupplierInfo, Invoice, Order, Returns
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'Glamour Cosmetics'


class SupplierInfoInline(admin.StackedInline):
    model = SupplierInfo
    can_delete = False
    verbose_name_plural = 'Supplier'


class CustomizedUserAdmin(UserAdmin):
    inlines = (SupplierInfoInline,)


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Newsupplier)
admin.site.register(SupplierProduct)
admin.site.register(OrderRequest)
admin.site.register(SupplierInfo)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Returns)