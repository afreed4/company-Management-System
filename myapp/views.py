from django.shortcuts import render,redirect,get_object_or_404
from django.http import request
from . import models
from . import forms
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import random
import json
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
User=get_user_model()
from django.contrib.auth.decorators import login_required
import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def employi_id():
    return random.randint(100000,900000)


def home(request):
    return render(request,'index.html')

#---------company management section-------------
#---company management's is superuser-----------
#---company management can add companys and Admin,HR,Manager for each company--------
#---company managers can login only with the superuser credentials-------


def company_management_login_view(request):
    if request.POST:
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
        
            if user is not None and user.staff_type=='company management':
                  login(request,user)
                  return redirect('company_manager_home')
            elif user is not None and user.is_staff==True:
                login(request,user)
                return redirect('company_manager_home')
            else:
             messages.warning(request,"Invalid Username Or Password")
             return render(request,'company_management/company_manager_login.html',{'form':form})
    else:
         form=AuthenticationForm()
    return render(request,'company_management/company_manager_login.html',{'form':form})


@login_required(login_url='/')
def company_manager_home(request):
    count=models.CompanyManagement.objects.all().count()
    username=request.user.username
    return render(request,'company_management/content.html',{'count':count,'username':username})


@login_required(login_url='/')
def update_company_count_company_manage(request):
    data=json.loads(request.GET.get('data','{}'))
    month=int(data.get('month'))
    year=int(data.get('year'))
   
    company_count=models.CompanyManagement.objects.filter(date_of_registration__year=year, date_of_registration__month=month).count()
    return JsonResponse({'company_count':company_count})


@login_required(login_url='/')
def update_staff_count_company_manage(request):
    data=json.loads(request.GET.get('data','{}'))
    month=int(data.get('month'))
    year=int(data.get('year'))
   
    staff_count=models.CustomUser.objects.filter(joined_date__year=year, joined_date__month=month).count()
    # print(f"Staff Count: {staff_count}")
    return JsonResponse({'staff_count':staff_count})


@login_required(login_url='/')
def add_company_view(request):
    if request.POST:
        form=forms.CompanyListing(request.POST,request.FILES)
        if form.is_valid():
            company_name=form.cleaned_data['company_name']
            if models.CompanyManagement.objects.filter(company_name__iexact=company_name).exists():
                messages.error(request, f"The company '{company_name}' already exists. Please choose a different name.")
                return render(request,'company_management/add_company.html',{'form':form})
            
            company=form.save(commit=False)
            company.save()
            
            default_departments=['Finance','Marketing','Sales','Customer service']
            for dept_name in default_departments:
                department, created=models.Department.objects.get_or_create(name=dept_name, for_company=company)
                
            messages.success(request, "Company added successfully.")
            return redirect('company_manager_home')
    else:
        form=forms.CompanyListing()
    return render(request,'company_management/add_company.html',{'form':form})


@login_required(login_url='/')
def read_and_edit_companys(request):
    companys=models.CompanyManagement.objects.all()
    return render(request,'company_management/company_view_and_edit.html',{'companys':companys})


@login_required(login_url='/')
def edit_company(request, id):
    company = get_object_or_404(models.CompanyManagement, id=id)
    if request.method == "POST":
        form = forms.CompanyListing(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully.")
            return redirect('edit_companys') 
        else:
            messages.error(request, "Check the details and try again.")
    else:
        form = forms.CompanyListing(instance=company)
    return render(request, 'company_management/edit_companys.html', {'form': form, 'id': id})


@login_required(login_url='/')
def view_companys(request,id):
    company =get_object_or_404(models.CompanyManagement,id=id)
    admin=company.staff_members.filter(staff_type='admin')
   
    return render(request,'company_management/view_company.html',{'company':company,'admin':admin})
        
        
@login_required(login_url='/')
def delete_companys(request,id):
    company=models.CompanyManagement.objects.get(id=id)
    try:
     company.delete()
     messages.error(request,'Company Deleted Successfully')
     return redirect('read_edit_company')
    except:
        messages.error(request,'"Failed to Delete Company."')
        return redirect('read_edit_company')
    

@login_required(login_url='/')
def update_company_reg(request):
    data_param = request.GET.get('data')
    data = json.loads(data_param)
    
    month = data['month']
    year = data['year']
    registartion_count=models.CompanyManagement.objects.filter(date_of_registration__month=month, date_of_registration__year=year).count()
    data={'enquiry_count_chart':registartion_count}
    return JsonResponse(data)


@login_required(login_url='/')
def add_staff(request):
    return render(request,'company_management/add_staff.html')


@login_required(login_url='/')
def staff_view(request):
    staff_details=models.CustomUser.objects.all()
    return render(request,'company_management/staff_view.html',{'staff_details':staff_details})


@login_required(login_url='/')
def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_staff')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        existing_user = models.CustomUser.objects.filter(username=username).exists()
        
        if existing_user:
            messages.error(request, "Username already exists. Please try another username.")
            return redirect('add_staff')

        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        staff_type = request.POST.get('staff_type')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        department_role=request.POST.get('manager_specialization')
        
       
        try:
                company = models.CompanyManagement.objects.get(company_name=company_name)
        except models.CompanyManagement.DoesNotExist:
                messages.error(request, 'Company does not exist.')
                return redirect('add_staff')
            
        if staff_type=='manager' and department_role==None:
            messages.error(request, "Please select a department role")
            
        if  staff_type=='manager':
            if not department_role:
                messages.error(request,'select departments only for managers')
                return redirect('add_staff')
            
            try:
                department=models.Department.objects.get(name=department_role, for_company=company)
            except models.Department.DoesNotExist:
                messages.error(request,'Selected Department Does Not Exist for the  company')
                return redirect('add_staff')
               
            user = models.CustomUser.objects.create_user(
                username=username, 
                password=password,
                staff_type=staff_type,
                contact_number=contact_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_role=department,
            )
            
            # Associate user with company
            company.staff_members.add(user)
            user.company = company
            user.save()
            
            messages.success(request, 'User created successfully.')
            return redirect('company_manager_home')
        
        else:
            # try:
            #     company = models.CompanyManagement.objects.get(company_name=company_name)
            # except models.CompanyManagement.DoesNotExist:
            #     messages.error(request, 'Company does not exist.')
            #     return redirect('add_staff')
            
            user = models.CustomUser.objects.create_user(
                username=username, 
                password=password,
                staff_type=staff_type,
                contact_number=contact_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            
            # Associate user with company
            company.staff_members.add(user)
            user.company = company
            user.save()
            
            messages.success(request, 'User created successfully.')
            return redirect('company_manager_home')
    


@login_required(login_url='/')
def edit_staff_view(request,id):
    staff = get_object_or_404(models.CustomUser, id=id)
    if request.method == "POST":
        form = forms.EditStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully.")
            return redirect('edit_companys')  
        else:
            messages.error(request, "Check the details and try again.")
    else:
        form = forms.EditStaffForm(instance=staff)
    company_name=staff.company.company_name if staff.company else None
    return render(request, 'company_management/edit_staff.html', {'form': form, 'id': id,'company_name':company_name})


@login_required(login_url='/')
def delete_staff(request,id):
    staff=models.CustomUser.objects.get(id=id)
    try:
     staff.delete()
     messages.error(request,'Staff Deleted Successfully')
     return redirect('staff_view')
    except:
        messages.error(request,"Failed to Delete Staff.")
        return redirect('staff_view')
    
#-------------End of company Management section---------------

#-------------start of Admin Section------------------------

#----------admin adds Manager and HR for admins company---------
#-----------Manager will add employees to thire department----------- 



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.staff_type == 'admin':
             login(request, user)
             return redirect('admin_home')
        elif user is not None and user.is_staff == True:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.warning(request,'Check username and password ¯\_(ツ)_/¯')
            return redirect('admin_login')
    return render(request,'admin_templates/admin_login.html')


@login_required(login_url='/')
def update_staff_count(request):
    data = json.loads(request.GET.get('data', '{}'))
    month = int(data.get('month'))
    year = int(data.get('year'))
    
    # Get the company of the current user (admin)
    company = request.user.company
    
    # Filter staff members by company, month, and year
    staff_count = models.CustomUser.objects.filter(
        company=company,
        joined_date__year=year,
        joined_date__month=month
    ).count()
    
    return JsonResponse({'staff_count': staff_count})


@login_required(login_url='/')
def admin_home(request):
    company_details=None
    staff_count=0
    if request.user.staff_type=='admin':
        company=request.user.company
        company_details=get_object_or_404(models.CompanyManagement, id=company.id)
        staff_count=models.CustomUser.objects.filter(company=company).count()
        username=request.user.username
    return render(request,'admin_templates/admin_home.html',{'company_details':company_details,'staff_count':staff_count,'username':username})


@login_required(login_url='/')
def admin_company_view(request):
    if request.user.staff_type == 'admin':
        company=request.user.company
        staff_members=models.CustomUser.objects.filter(company=company)
        company_details=get_object_or_404(models.CompanyManagement, id=company.id)
    else:
        return redirect('admin_home')
    return render(request,'admin_templates/admin_company_view.html',{'staff_members':staff_members,'company_details':company_details})


@login_required(login_url='/')
def admin_edit_companys(request, id):
    company = get_object_or_404(models.CompanyManagement, id=id)
    if request.method == "POST":
        form = forms.CompanyListing(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully.")
            return redirect('edit_companys') 
        else:
            messages.error(request, "Check the details and try again.")
    else:
        form = forms.CompanyListing(instance=company)

    return render(request, 'admin_tmplates/edit_company.html', {'form': form, 'id': id})


@login_required(login_url='/')
def admin_add_staff(request):
    return render(request,'admin_templates/add_staff.html')


@login_required(login_url='/')
def admin_add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('admin_add_staff')
    else:
        
        username = request.POST['username']
        password = request.POST['password']
        
        existing_user=models.CustomUser.objects.filter(username=username).first()
        
        if existing_user:
            messages.error(request, "Username already exists. Please try another username.")
            return redirect('admin_add_staff')
        
        else:
       
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         staff_type = request.POST.get('staff_type')
         contact_number = request.POST.get('contact_number')
         email = request.POST.get('email')
         #company_name = request.POST.get('company_name')
         department_role_name=request.POST.get('manager_specialization')
         company=request.user.company
         
         if staff_type=='manager':
                department_role=None
                if department_role_name:
                    departments=models.Department.objects.filter(name=department_role_name)
                    
                    if departments.exists():
                        department_role=departments.first()
                    else:
                        messages.error(request, "Department does not exist. Please add the department first.")
                        return redirect('admin_add_staff')
              
         
             
                user = models.CustomUser.objects.create_user(
                    username=username, 
                    password=password,
                    staff_type=staff_type,
                    contact_number=contact_number,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        department_role=department_role,
                        #employee_id=employi_id()  
                    )
                user.company=company
                user.save()
                messages.success(request,'User created successfully')
                return redirect('admin_home')
            
         else: 
           user = models.CustomUser.objects.create_user(
            username=username, 
            password=password,
            staff_type=staff_type,
            contact_number=contact_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            #employee_id=employi_id()  
        )
           user.company=company
           user.save()
           messages.success(request,'User created successfully')
           return redirect('admin_home')
    
    
@login_required(login_url='/')
def admin_staff_view(request):
    if request.user.staff_type=='admin':
        company=request.user.company
        staff_members=models.CustomUser.objects.filter(company=company)
    return render(request,'admin_templates/staff_view.html',{'staff_members':staff_members,'company':company})


@login_required(login_url='/')
def admin_edit_staff_view(request,id):
    staff = get_object_or_404(models.CustomUser, id=id)
    if request.method == "POST":
        form = forms.EditStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff details updated successfully.")
            return redirect('admin_staff_view')  
        else:
            messages.error(request, "Check the details and try again.")
    else:
        form = forms.EditStaffForm(instance=staff)
    company_name=staff.company.company_name if staff.company else None
    return render(request, 'admin_templates/edit_staff.html', {'form': form, 'id': id,'company_name':company_name})



@login_required(login_url='/')
def admin_delete_staff(request,id):
    staff=models.CustomUser.objects.get(id=id)
    try:
     staff.delete()
     messages.error(request,'Staff Deleted Successfully')
     return redirect('admin_staff_view')
    except:
        messages.error(request,"Failed to Delete Staff.")
        return redirect('admin_staff_view')


@login_required(login_url='/')
def compalints_view(request):
   if request.user.staff_type == 'admin':
       
        company=request.user.company
        staff_members=models.Complaints.objects.filter(for_company=company)
        company_details=get_object_or_404(models.CompanyManagement, id=company.id)
        
        complaints_data = []
        for staff in staff_members:
            if staff.complaints:  
                complaints_data.append({
                    'username': staff.send_by.username,
                    # 'staff_type': staff.staff_type,
                    'complaints': staff.complaints,
                })
                
   else:
        return redirect('admin_home')
   return render(request,'admin_templates/complaints.html',{'complaints_data':complaints_data,})



@login_required(login_url='/')
def complaints_count_view(request):
    month=request.GET.get('month')
    year=request.GET.get('year')
    company=request.user.company
    
    complaints_count=models.Complaints.objects.filter(
        for_company=company,
        send_by__joined_date__year=year,
        send_by__joined_date__month=month
    ).count()
    
    return JsonResponse({'complaints_count':complaints_count})

#-----------end of admin section---------------------

#-----------start of manager section----------------



def manager_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.staff_type == 'manager':
             login(request, user)
             return redirect('manager_home')
        elif user is not None and user.is_staff == True:
            login(request, user)
            return redirect('manager_home')
        else:
            messages.warning(request,'Check username and password ¯\_(ツ)_/¯')
            return redirect('manager_login')
    return render(request,'manager_templates/manager_login.html')



@login_required(login_url='/')
def manager_home(request):
    username=request.user.username
    staff_details=models.CustomUser.objects.none()
    company=None
    department=None
    managers=None
    if request.user.staff_type=='manager':
        company=request.user.company
        department=request.user.department_role
        staff_details=models.CustomUser.objects.filter(company=company, department_role=request.user.department_role,staff_type='employee')
        managers=models.CustomUser.objects.filter(company=company, department_role=request.user.department_role,staff_type='manager')
        username=request.user.username
        return render(request,'manager_templates/manager_home.html',{'staff_details':staff_details,'department':department,'username':username,'company':company,'managers':managers})
    return render(request,'manager_templates/manager_home.html',{'staff_details':staff_details,'department':department,'username':username,'company':company,'managers':managers})


@login_required(login_url='/')
def manager_add_staff(request):
    return render(request,'manager_templates/add_employees.html')


@login_required(login_url='/')
def manager_add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('manager_add_staff')
    else:
        
        username = request.POST['username']
        password = request.POST['password']
        
        existing_user=models.CustomUser.objects.filter(username=username).first()
        
        if existing_user:
            messages.error(request, "Username already exists. Please try another username.")
            return redirect('manager_add_staff')
        
        else:
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         contact_number = request.POST.get('contact_number')
         email = request.POST.get('email')
         salary=request.POST.get('salary')
         
         company=request.user.company
         
         department_role = request.user.department_role
         print(department_role)
         if department_role is not None and not isinstance(department_role,models.Department):
             department_role = models.Department.objects.filter(name=department_role).first()
        
         user = models.CustomUser.objects.create_user(
            username=username, 
            password=password,
            staff_type='employee',
            contact_number=contact_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_role=department_role,
            #employee_id=employi_id(),
            salary=salary  
        )
         user.company=company
         user.save()
         messages.success(request,'User created successfully')
         return redirect('manager_add_staff')
    
    
@login_required(login_url='/')
def manager_edit_staff(request,id):
     staff = get_object_or_404(models.CustomUser, id=id)
     if request.method == "POST":
        form = forms.ManagerEditStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff details updated successfully.")
            return redirect('manager_home')  
        else:
            messages.error(request, "Check the details and try again.")
     else:
        form = forms.ManagerEditStaffForm(instance=staff)
     employees_id=staff.employee_id
     return render(request, 'manager_templates/edit_staff.html', {'form': form, 'employees_id': employees_id})
 
 
@login_required(login_url='/')
def attendance(request):
      if request.user.staff_type=='manager':
        company=request.user.company
        department=request.user.department_role
        staff_details=models.CustomUser.objects.filter(company=company, department_role=request.user.department_role, staff_type='employee')
      return render(request,'manager_templates/attendance.html',{'staff_details':staff_details,'department':department})
  

@login_required(login_url='/')
def take_attendance(request, id):
    staff = get_object_or_404(models.CustomUser, id=id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        date = timezone.now().date()
        
        # Get or create attendance record for today
        attendancee, created = models.Attendance.objects.get_or_create(
            connection=staff,
            attendence_date=date
        )
        
        if action == 'clock_in':
            if attendancee.clock_in is None:
                attendancee.clock_in = timezone.now()
                attendancee.save()
                return JsonResponse({'success': f'{staff.username} clocked in successfully!'}, status=200)
            else:
                return JsonResponse({'error': 'Already clocked in today'}, status=400)
        
        elif action == 'clock_out':
            if attendancee.clock_in is not None and attendancee.clock_out is None:
                attendancee.clock_out = timezone.now()
                attendancee.save()
                return JsonResponse({'success': f'{staff.username} clocked out successfully!'}, status=200)
            elif attendancee.clock_in is None:
                return JsonResponse({'error': 'Cannot clock out without clocking in'}, status=400)
            else:
                return JsonResponse({'error': 'Already clocked out today'}, status=400)
        
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    return render(request, 'manager_templates/take_attendance.html', {'id': id})

 
@login_required(login_url='/')
def attendance_report(request,id):
    staff =get_object_or_404(models.CustomUser, id=id)
    attendance_record=models.Attendance.objects.filter(connection__id=id)
    paginator=Paginator(attendance_record,15)
    page=request.GET.get('page')
    try:
        items=paginator.page(page)
    except PageNotAnInteger:
        items=paginator.page(1)
    except EmptyPage:
        items=paginator.page(paginator.num_pages)
    return render(request, 'manager_templates/attendance_report.html', {'items':items, 'staff':staff})


@login_required(login_url='/')
def leave_request_view(request):
    department=None
    leave_request=None
    if request.user.staff_type=='manager':
        department=request.user.department_role
        leave_request=models.LeaveRequest.objects.filter(department=department)
        print("manager",leave_request)
        return render(request,'manager_templates/leave_request.html',{'leave_request':leave_request})
    return render(request,'manager_templates/leave_request.html',{'leave_request':leave_request})


@login_required(login_url='/')
def replay_for_leave_request(request,id):
     leave_request=get_object_or_404(models.LeaveRequest, id=id)
     if request.POST:
         form=forms.ReplayForLeaveForm(request.POST)
         if form.is_valid():
             response=form.cleaned_data['response']
             leave_request.response=response
             leave_request.responsed_date = timezone.now()
             leave_request.save()
             messages.success(request,'Leave request submitted successfully')
             return redirect('leave_request_view')
         else:
            messages.error(request,'Somthing went wrong please try again')
            return redirect('leave_request_view')
     else:
         form=forms.ReplayForLeaveForm()
     return render(request,'manager_templates/replay_for_leave.html',{'form':form})
 
#---------------end of manager-------------------------

#----------------start of HR section-------------



def hr_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.staff_type == 'hr':
             login(request, user)
             return redirect('hr_home')
        elif user is not None and user.is_staff == True:
            login(request, user)
            return redirect('hr_home')
        else:
            messages.warning(request,'Check username and password ¯\_(ツ)_/¯')
            return redirect('hr_login')
    return render(request,'hr_templates/hr_login.html')


@login_required(login_url='/')
def hr_home(request):
    staff_details=models.CustomUser.objects.none()
    username=request.user.username
    company=None
    
    if request.user.staff_type=='hr':
        company=request.user.company
        username=request.user.username
        staff_details=models.CustomUser.objects.filter(company=company)
        
    return render(request,'hr_templates/hr_home.html',{'staff_details':staff_details,'username':username,'company':company})
   


@login_required(login_url='/')
def hr_manage_staff(request):
    if request.user.staff_type=='hr':
        company=request.user.company
        staff_details=models.CustomUser.objects.filter(company=company)
    return render(request,'hr_templates/manage_staff.html',{'staff_details':staff_details})


@login_required(login_url='/')
def hr_edit_staff(request,id):
    staff = get_object_or_404(models.CustomUser, id=id)
    if request.method == "POST":
        form = forms.HrEditStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff details updated successfully.")
            return redirect('hr_manage_staff')  
        else:
            messages.error(request, "Check the details and try again.")
    else:
        form = forms.HrEditStaffForm(instance=staff)
    return render(request, 'hr_templates/hr_edit_staff.html', {'form': form, 'id': id,})



@login_required(login_url='/')
def hr_delete_staff(request,id):
    staff=models.CustomUser.objects.get(id=id)
    try:
     staff.delete()
     messages.error(request,'Staff Deleted Successfully')
     return redirect('hr_manage_staff')
    except:
        messages.error(request,"Failed to Delete Staff.")
        return redirect('hr_manage_staff')


@login_required(login_url='/')
def hr_add_employees(request):
    if request.POST:
        form=forms.HrAddEmployeesForm(request.POST, user=request.user)
        if form.is_valid():
            employee=form.save(commit=False)
            
            if request.user.staff_type == 'hr':
                employee.company = request.user.company
            
            password=form.cleaned_data.get('password')
            employee.set_password(password)
            
            employee.save()
            messages.success(request,'Employee created successfully')
            return redirect('hr_add_employees')
        else:
            messages.error(request,'Failed to create employee')
            return redirect('hr_add_employees')
    else:
        form=forms.HrAddEmployeesForm(user=request.user)
    return render(request,'hr_templates/hr_add_staff.html',{'form':form})



@login_required(login_url='/')
def create_department(request):
    if request.POST:
        form=forms.CreateDepartment(request.POST)
        if form.is_valid():
            department=form.save(commit=False)
            hr_user=request.user
            
            if hr_user.company:
                department.for_company=hr_user.company
                department.save()
                messages.success(request,'Department created successfully')
            else:
                messages.error(request,'HR company not found. Unable to create new department')
        else:
            messages.error(request,'Failed to create department')
    else:
        form=forms.CreateDepartment()
    return render(request,'hr_templates/create_department.html',{'form':form})


@login_required(login_url='/')
def manage_department(request):
    if request.user.staff_type=='hr':
        company=request.user.company
        staff_details=models.CustomUser.objects.filter(company=company)
        department=models.Department.objects.filter(for_company=company)
        print(department)
        return render(request,'hr_templates/manage_department.html',{'department':department,'staff_details':staff_details})
    
    return render(request,'hr_templates/manage_department.html')


@login_required(login_url='/')
def edit_department(request,id):
    department=get_object_or_404(models.Department, id=id)
    if request.POST:
        form=forms.EditDepartmentForm(request.POST,instance=department)
        if form.is_valid():
            form.save()
            messages.success(request,'Department updated successfully')
            return redirect('edit_department',id=id)
        else:
            messages.error(request,'Somthing went wrong please try again ')
    else:
        form=forms.EditDepartmentForm(instance=department)
    return render(request,'hr_templates/edit_department.html',{'form':form})

def delete_department(request,id):
    department=models.Department.objects.get(id=id)
    try:
     department.delete()
     messages.error(request,'Staff Deleted Successfully')
     return redirect('delete_department',id=id)
    except:
        messages.error(request,"Failed to Delete Staff.")
        return redirect('delete_department',id=id)
    
    
#------------end of HR section---------------------

#-------------start of Employee-------------------

def employee_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.staff_type == 'employee':
             login(request, user)
             return redirect('employee_home')
        elif user is not None and user.is_staff == True:
            login(request, user)
            return redirect('employee_home')
        else:
            messages.warning(request,'Check username and password ¯\_(ツ)_/¯')
            return redirect('employee_login')
     return render(request,'employee_templates/employee_login.html')
 
 
 
@login_required(login_url='/')
def employee_home(request):
    employee_details=models.CustomUser.objects.none()
    username=request.user.username
    company=None
    department=None
    
    if request.user.staff_type=='employee':
        company=request.user.company
        username=request.user.username
        employee_details=models.CustomUser.objects.get(username=username)
        department=request.user.department_role
        
    return render(request,'employee_templates/employee_home.html',{'company':company, 'username':username, 'employee_details':employee_details,'department':department})




@login_required(login_url='/')
def request_leave(request):
    if request.POST:
        form=forms.LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request=form.save(commit=False)
            employee=request.user
            leave_request.requested_by=employee
            leave_request.department=employee.department_role
            leave_request.requested_date=timezone.now()
            
            manager=models.CustomUser.objects.filter(department_role=employee.department_role, staff_type='manager').first()
            leave_request.department=request.user.department_role
            leave_request.save()
            
           
            
            messages.success(request,'Leave request submitted successfully')
            return redirect('request_leave')
        else:
            messages.error(request,'Somthing went wrong please try again')
            return redirect('request_leave')
    else:
        form=forms.LeaveRequestForm()
    return render(request,'employee_templates/request_leave.html',{'form':form})


@login_required(login_url='/')
def about_leave(request):
    employee = request.user
    leave_requests = models.LeaveRequest.objects.filter(requested_by=employee)
    print(leave_requests)
    return render(request, 'employee_templates/leave.html', {'leave_requests': leave_requests})


@login_required(login_url='/')
def send_compalints(request):
    if request.POST:
        form=forms.ComplaintForm(request.POST)
        if form.is_valid():
            complaint=form.save(commit=False)
            complaint.send_by=request.user
            complaint.save()
            messages.success(request,'Complaint registerd successfully')
            return redirect('send_compalints')
        else:
            messages.error(request,'Somthing went wrong please try again')
            return redirect('send_compalints')
    else:
        form=forms.ComplaintForm()
    return render(request,'employee_templates/complaint.html',{'form':form}) 
        
        
@login_required(login_url='/')
def employee_attendance_report_view(request):
    if request.user.staff_type=='employee':
        attendance_record=models.Attendance.objects.filter(connection=request.user)
        paginator=Paginator(attendance_record,15)
        page=request.GET.get('page')
        try:
            items=paginator.page(page)
        except PageNotAnInteger:
            items=paginator.page(1)
        except EmptyPage:
            items=paginator.page(paginator.num_pages)
        return render(request, 'employee_templates/attendance_report.html', {'items':items})
    
    
@login_required(login_url='/')
def edit_profile_employee(request):
    if request.POST:
        form=forms.CustomUserChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updations Successfull !')
            return redirect('edit_profile')
        else:
            messages.error(request,'Somthing went wrong please try again')
            return redirect('edit_profile')
    else:
        form=forms.CustomUserChangeForm(instance=request.user)
    return render(request,'employee_templates/profile.html',{'form':form})
 
 
@login_required(login_url='/')
def change_password(request):
    if request.POST:
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Password Change Successfully")
            return redirect('edit_profile_employee')
        else:
            messages.error(request,"Somthing went wrong please try again")
            return redirect('edit_profile_employee')
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'employee_templates/change_pass.html',{'form':form})

@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')