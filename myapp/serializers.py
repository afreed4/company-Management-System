from rest_framework import serializers
from .models import CompanyManagement, CustomUser,Complaints,Attendance,LeaveRequest,Department

class CompanyManagementserializers(serializers.ModelSerializer):
    class Meta:
        model=CompanyManagement
        fields='__all__'
        
class CustomUserserializers(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'
        
class Complaintsserializers(serializers.ModelSerializer):
    class Meta:
        model=Complaints
        fields='__all__'
        
class Attendanceserializers(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields='__all__'
        
class LeaveRequestserializers(serializers.ModelSerializer):
    class Meta:
        model=LeaveRequest
        fields='__all__'
        
class Departmentserializers(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'
