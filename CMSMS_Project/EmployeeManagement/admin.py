from django.contrib import admin
from .models import Employees, Department, Position
from .models import *


admin.site.register(Employees)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Attendance)

