from django.contrib import admin


# Register your models here.
from .models import *

admin.site.register(products)
admin.site.register(formulation)
admin.site.register(lab_test)
admin.site.register(harmfull_chemicals)
admin.site.register(equipments)
admin.site.register(test_chemicals)
admin.site.register(schedule_test)
admin.site.register(schedule_test_chemicals)
admin.site.register(products_history)
admin.site.register(formulationhistory)