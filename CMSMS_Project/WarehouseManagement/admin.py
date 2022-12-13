from django.contrib import admin
from .models import Product, WarehouseRequest, RawMaterial, Equipment, Packaging, WarehouseEmployee, History


admin.site.register(Product)
admin.site.register(WarehouseRequest)
admin.site.register(RawMaterial)
admin.site.register(Equipment)
admin.site.register(Packaging)
admin.site.register(WarehouseEmployee)
admin.site.register(History)
