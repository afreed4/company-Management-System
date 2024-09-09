from rest_framework import viewsets
from . models import CompanyManagement,CustomUser,Attendance,LeaveRequest,Department,Complaints
from . serializers import CompanyManagementserializers,CustomUserserializers,Attendanceserializers,Departmentserializers,LeaveRequestserializers,Complaintsserializers
from rest_framework.permissions import IsAuthenticated

class CompanyViewSet(viewsets.ModelViewSet):
    queryset=CompanyManagement.objects.all()
    serializer_class = CompanyManagementserializers
    permission_classes = [IsAuthenticated]
    
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class = CustomUserserializers
    permission_classes = [IsAuthenticated]
    
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class = Departmentserializers
    permission_classes = [IsAuthenticated]
    
class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset=LeaveRequest.objects.all()
    serializer_class = LeaveRequestserializers
    permission_classes = [IsAuthenticated]
    
class ComplaintsViewSet(viewsets.ModelViewSet):
    queryset=Complaints.objects.all()
    serializer_class = Complaintsserializers
    permission_classes = [IsAuthenticated]
    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset=Attendance.objects.all()
    serializer_class = Attendanceserializers
    permission_classes = [IsAuthenticated]