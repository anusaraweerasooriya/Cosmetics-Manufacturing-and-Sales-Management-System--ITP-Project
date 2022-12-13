from django.contrib import admin
from .models import *

admin.site.register(RawMaterial)
admin.site.register(Request)
admin.site.register(ScheduleProduction)
admin.site.register(Batch)
admin.site.register(Machine)
admin.site.register(RawMaterialHistory)
admin.site.register(RequestHistory)
