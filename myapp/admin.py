from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CompanyManagement)
admin.site.register(CustomUser)
admin.site.register(Attendance)
admin.site.register(Complaints)
admin.site.register(LeaveRequest)