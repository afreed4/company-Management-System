
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    #----company management urls----------
    path('company_managemnt_login/',views.company_management_login_view,name='home'),
    path('company_management_home/',views.company_manager_home,name='company_manager_home'),
    path('add_company/',views.add_company_view,name='add_company'),
    path('view_companys/<int:id>/',views.view_companys,name='view_companys'),
    path('read_edit_company/',views.read_and_edit_companys,name='read_edit_company'),
    path('edit_companys/<int:id>/',views.edit_company,name='edit_companys'),
    # path('edit_companys_save/<int:id>/',views.edit_companys_save,name='edit_companys_save'),
    path('delete_companys/<int:id>/',views.delete_companys,name='delete_companys'),
    path('update_company_reg/',views.update_company_reg,name='update_company_reg'),
    path('add_staff_save/',views.add_staff_save,name='add_staff_save'),
    path('add_staff/',views.add_staff,name='add_staff'),
    path('staff_view/',views.staff_view,name='staff_view'),
    path('edit_staff/<int:id>/',views.edit_staff_view,name='edit_staff'),
    path('delete_staff/<int:id>/',views.delete_staff,name='delete_staff'),
    path('update_company_count_company_manage/',views.update_company_count_company_manage,name='update_company_count_company_manage'),
    path('update_staff_count_company_manage/',views.update_staff_count_company_manage,name='update_staff_count_company_manage'),
    
    #------end of company management------------
    
    #-------start of admin section-------------
    
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_company_view/',views.admin_company_view,name='admin_company_view'),
    path('admin_edit_companys<int:id>/',views.admin_edit_companys,name='admin_edit_companys'),
    path('admin_add_staff/',views.admin_add_staff,name='admin_add_staff'),
    path('admin_add_staff_save/',views.admin_add_staff_save,name='admin_add_staff_save'),
    path('update_staff_count/',views.update_staff_count,name='update_staff_count'),
    path('admin_staff_view/',views.admin_staff_view,name='admin_staff_view'),
    path('admin_edit_staff_view/<int:id>/',views.admin_edit_staff_view,name='admin_edit_staff_view'),
    path('admin_delete_staff/<int:id>/',views.admin_delete_staff,name='admin_delete_staff'),
    path('compalints_view/',views.compalints_view,name='compalints_view'),
    path('complaints_count_view/',views.complaints_count_view,name='complaints_count_view'),
    
    #----------end of admin section----------------
    
    #----------start of manager section------------
    
    path('manager_login/',views.manager_login,name='manager_login'),
    path('manager_home/',views.manager_home,name='manager_home'),
    path('manager_add_staff/',views.manager_add_staff,name='manager_add_staff'),
    path('manager_add_staff_save/',views.manager_add_staff_save,name='manager_add_staff_save'),
    #path('manager_side_bar/',views.manager_side_bar,name='manager_side_bar'),
    path('manager_edit_staff/<int:id>/',views.manager_edit_staff,name='manager_edit_staff'),
    path('attendance/',views.attendance,name='attendance'),
    path('take_attendance/<int:id>/',views.take_attendance,name='take_attendance'),
    path('attendance_report/<int:id>/',views.attendance_report,name='attendance_report'),
    path('leave_request_view/',views.leave_request_view,name='leave_request_view'),
    path('replay_for_leave_request/<int:id>/',views.replay_for_leave_request,name='replay_for_leave_request'),
    
    #-----------end of manager section----------------------
    
    #-----------start of HR section----------------------
    
    path('hr_login/',views.hr_login,name='hr_login'),
    path('hr_home/',views.hr_home,name='hr_home'),
    path('hr_manage_staff/',views.hr_manage_staff,name='hr_manage_staff'),
    path('hr_edit_staff/<int:id>/',views.hr_edit_staff,name='hr_edit_staff'),
    path('hr_delete_staff/<int:id>/',views.hr_delete_staff,name='hr_delete_staff'),
    path('hr_add_employees/',views.hr_add_employees,name='hr_add_employees'),
    path('create_department/',views.create_department,name='create_department'),
    path('manage_department/',views.manage_department,name='manage_department'),
    path('edit_department/<int:id>/',views.edit_department,name='edit_department'),
    path('delete_department/<int:id>/',views.delete_department,name='delete_department'),
    
    #--------------end of HR section-------------------------
    #--------------start of Employee section-----------------
    
    path('employee_login/',views.employee_login,name='employee_login'),
    path('employee_home/',views.employee_home,name='employee_home'),
    path('request_leave/',views.request_leave,name='request_leave'),
    path('about_leave/',views.about_leave,name='about_leave'),
    path('send_compalints/',views.send_compalints,name='send_compalints'),
    path('employee_attendance_report_view/',views.employee_attendance_report_view,name='employee_attendance_report_view'),
    path('edit_profile_employee/',views.edit_profile_employee,name='edit_profile_employee'),
    path('change_pass/',views.change_password,name='change_pass'),
    
    path('logout_user/',views.logout_user,name='logout_user')
]
