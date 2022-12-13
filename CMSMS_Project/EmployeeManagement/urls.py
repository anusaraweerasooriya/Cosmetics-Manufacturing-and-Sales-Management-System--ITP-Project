from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    # path('', views.home, name="home-page"),
    path('',views.dashboard, name="dashboard"),
    path('login/', auth_views.LoginView.as_view(template_name = 'EmployeeManagement/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin/', views.login_user, name="login-user"),
    path('logout/', views.logoutuser, name="logout"),
    path('about/', views.about, name="about-page"),
    path('departments/', views.departments, name="department-page"),
    path('manage_departments/', views.manage_departments, name="manage_departments-page"),
    path('save_department/', views.save_department, name="save-department-page"),
    path('delete_department/', views.delete_department1, name="delete-department"),
    path('positions/', views.positions, name="position-page"),
    path('manage_positions/', views.manage_positions, name="manage_positions-page"),
    path('save_position/', views.save_position, name="save-position-page"),
    path('delete_position/', views.delete_position, name="delete-position"),
    path('employees/', views.employees, name="employee-page"),
    path('admin', views.home, name="home-page"),
    path('attendance/', views.attendance, name="employee-attendance"),
    path('leave/', views.leave, name="employee-leave"),
    path('approve-leave', views.approveleave, name="approve-leave"),
    path('reject-leave', views.rejectleave, name="reject-leave"),
    path('employees1', views.employees1, name="employee1"),
    path('save-attendance', views.saveAttendance, name="save-attendance"),
    path('save-leave', views.saveLeave, name="save-Leave"),
    path('user/', views.user, name="user"),
    path('manage_employees/', views.manage_employees, name="manage_employees-page"),
    path('save_employee/', views.save_employee, name="save-employee-page"),
    path('delete_employee/', views.delete_employee, name="delete-employee"),
    path('view_employee/', views.view_employee, name="view-employee-page"),


]
