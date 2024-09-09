from typing import Any
from django import forms
from . models import CompanyManagement,CustomUser,Department,LeaveRequest,Complaints
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class SighnupForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','password1','password2']
        
class LoginForm(forms.Form):
    username=forms.CharField(max_length=225)
    password=forms.CharField(max_length=200, widget=forms.PasswordInput)
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=['username','email','contact_number']
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
            'contact_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Contact Number'}),
        }
        
class CompanyListing(forms.ModelForm):
    class Meta:
        model=CompanyManagement
        fields=['company_name','address','contact_number','email','logo','company_code_for_employee_id']
        
        widgets={
        'company_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Company Name'}),
        'address':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Commpany Adress'}),
        'contact_number':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Company Contact Number'}),
        'email':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Email adress'}),
        'company_code_for_employee_id':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Company Code for Employee ID'}),
        }
        
class EditStaffForm(forms.ModelForm):
    company=forms.ModelChoiceField(queryset=CompanyManagement.objects.all(),required=False)
    class Meta:
        model=CustomUser
        fields=['staff_type','contact_number','first_name','last_name','company']
        
        widgets={
            'first_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Last Name'}),
            'contact_number':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Contact Number'}),
            'staff_type':forms.Select(choices=[('Admin','Admin'),('HR','HR'),('Manager','Manager')],attrs={'class': 'form-control class1', 'placeholder': 'Staff Type'}),
            'company':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Company Name'})
        }
        
class ManagerEditStaffForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','contact_number','salary','email']
        
        widgets={
            'first_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Last Name'}),
            'contact_number':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Contact Number'}),
            'salary':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Salary'}),
            'email':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'email'})
        }
        
class EditDepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields=['name']
    
        widgets={
            'name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Department Name'})
        }
        
class HrEditStaffForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','contact_number','salary','email','department_role']
        
        widgets={
            'first_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Last Name'}),
            'contact_number':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Contact Number'}),
            'salary':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Salary'}),
            'email':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'email'}),
        }
        
    department_role=forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control class1', 'placeholder': 'Departments'}),
        empty_label="Select Department",
        required=False
    )
    
class HrAddEmployeesForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control class1', 'placeholder': 'Password'})),
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control class1', 'placeholder': 'Password'}))
    
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','contact_number','salary','email','department_role','staff_type']
        widgets={
            'username':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Username'}),
            'first_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Last Name'}),
            'contact_number':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Contact Number'}),
            'salary':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Salary'}),
            'email':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder': 'Email'}),
            'staff_type':forms.TextInput(attrs={'class': 'form-control class1', 'readonly': 'readonly'}),
        }
    
    #this init methode is for only display the Departments which are assighned to HR
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user',None)
        super(HrAddEmployeesForm, self).__init__(*args, **kwargs)
        
        self.fields['department_role'].widget.attrs.update({
            'class':'form-control class1',
            'placeholder':'Select Department',
            'required':True
        })
        
        if user and user.staff_type=='hr':
            self.fields['department_role'].queryset=Department.objects.filter(for_company=user.company)
        else:
            self.fields['department_role'].queryset=Department.objects.none()
        
    
        self.fields['staff_type'].initial='employee'
        self.fields['staff_type'].disabled=True
        
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        # confirm_password=cleaned_data.get('confirm_password')
        
        # if password and confirm_password and password !=confirm_password:
        #     self.add_error('confirm_password', 'Password do not match')
        
        return cleaned_data
    
class CreateDepartment(forms.ModelForm):
    class Meta:
        model=Department
        fields=['name']
        widgets={
            'name':forms.TextInput(attrs={'class': 'form-control class1', 'placeholder':'Department Name'})
        }
        
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model=LeaveRequest
        fields=['request']
        
        widgets={
            'request':forms.Textarea(attrs={'class':'form-control class1','placeholder':'Write your request for leave'}),
        }
        
class ReplayForLeaveForm(forms.ModelForm):
     class Meta:
        model=LeaveRequest
        fields=['response']
        
        widgets={
            'response':forms.Textarea(attrs={'class':'form-control class1','placeholder':'Write your response for leave'}),
        }
        
class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaints
        fields=['complaints']
        
        widgets={
            'complaints':forms.Textarea(attrs={'class':'form-control class1','placeholder':'Write your compalint here'})
        }