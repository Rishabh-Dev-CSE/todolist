from django.contrib import admin
from . models import *

class CustomAdmin(admin.ModelAdmin):
    list_display = ['user_id','email', 'is_staff', 'is_active', 'manager_code']
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['manager_id','employee_id','employee_name','employee_email']

admin.site.register(CustomUser, CustomAdmin)

admin.site.register(BossCustomUser)

admin.site.register(EmployeeModel,EmployeeAdmin)

admin.site.register(ManagerToUserTask)

