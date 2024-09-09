from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
import random
from calendar import monthrange
import datetime
from django.utils import timezone
import re
import uuid
from django.utils import timezone

class CompanyManagement(models.Model):
    id=models.AutoField(primary_key=True)
    company_name=models.TextField()
    address=models.TextField()
    contact_number=models.CharField(max_length=15,null=True,blank=True)
    email=models.TextField()
    logo=models.FileField(upload_to='logo/')
    company_code_for_employee_id=models.CharField(max_length=5)
    date_of_registration=models.DateField(default=timezone.now)
    staff_members=models.ManyToManyField('CustomUser',related_name='companies')
    
    def __str__(self):
        return self.company_name
    
class Department(models.Model):
    name=models.CharField(max_length=255)
    for_company = models.ForeignKey(CompanyManagement, on_delete=models.SET_NULL, null=True, blank=True,)
    
    class Meta:
        unique_together = ('name', 'for_company')
    
    def __str__(self):
        return self.name

    
class CustomUser(AbstractUser):
    STAFF_TYPES=(
        ('admin','Administrator'),
        ('hr','HR'),
        ('manager','Manager'),
        ('employee','Employee'),
        ('company management','Company Management')
    )
    
    DEPARTMENT_TYPE=(
        ('finance','Finance'),
        ('marketing','Marketing'),
        ('sales','Sales'),
        ('customer service','Customer Service'),
    )
    staff_type=models.CharField(max_length=20,choices=STAFF_TYPES)
    contact_number=models.CharField(max_length=15,null=True,blank=True)
    company=models.ForeignKey(CompanyManagement,models.CASCADE,null=True,blank=True)
    
    employee_id=models.TextField(unique=True,null=True,blank=True)
    department_role = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    joined_date=models.DateField(blank=True,null=True,auto_now_add=True)
    salary=models.CharField(max_length=50,null=True,blank=True)
    
    
    def genarate_employee_id(self):
        return str(uuid.uuid4())[:6]
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id=self.genarate_employee_id()
            
        if self.is_superuser and self.staff_type != 'company management':
            self.staff_type='company management'
        super(CustomUser, self).save(*args, **kwargs)
    
    def __str__(self):
	    return self.username
 
class LeaveRequest(models.Model):
     request=models.TextField()
     requested_by=models.ForeignKey(CustomUser,models.DO_NOTHING,null=True,blank=True)
     response=models.TextField()
     requested_date=models.DateTimeField(auto_now_add=True)
     responsed_date=models.DateTimeField(null=True, blank=True)
     department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
     
     
class Complaints(models.Model):
     complaints=models.TextField(null=True)
     send_by=models.ForeignKey(CustomUser,models.CASCADE, null=True,blank=True)
     for_company=models.ForeignKey(CompanyManagement,models.CASCADE, null=True,blank=True)

class Attendance(models.Model):
    connection=models.ForeignKey(CustomUser,on_delete=models.CASCADE ,null=True,blank=True)
    updated_date=models.DateTimeField(default=timezone.now)
    attendence_date=models.DateField(auto_now_add=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('connection', 'attendence_date') 