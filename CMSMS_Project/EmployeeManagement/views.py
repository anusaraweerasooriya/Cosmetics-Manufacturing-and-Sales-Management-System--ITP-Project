import csv
import this

from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Department, Position, Employees, Attendance, Leave
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .decorators import employee_manager_only
import json


# Login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')


# ===========================  Chart =====================================


def home(request):
    departments_employee = Employees.objects.all()

    # Employee count in each department
    emp_managememt_count = Employees.objects.filter(department_id=4).count()
    warehouse_managememt_count = Employees.objects.filter(department_id=1).count()
    Delivery_Management_count = Employees.objects.filter(department_id=8).count()
    Sales_Management_count = Employees.objects.filter(department_id=2).count()
    Batch_Production_Management_count = Employees.objects.filter(department_id=6).count()
    Cost_Analysis_Management_count = Employees.objects.filter(department_id=7).count()
    Laboratory_Management_count = Employees.objects.filter(department_id=9).count()
    Supplier_Management_count = Employees.objects.filter(department_id=10).count()

    # #### department list
    department_list = ['Employee', 'Warehouse', 'Delivery', 'Sales', 'Batch Production', 'Cost Analysis', 'Laboratory',
                       'Supplier']

    # ######## count list
    employee_count = [emp_managememt_count, warehouse_managememt_count, Delivery_Management_count,
                      Sales_Management_count, Batch_Production_Management_count, Cost_Analysis_Management_count,
                      Laboratory_Management_count, Supplier_Management_count]

    context = {
        'page_title': 'Home',
        'departments_employee': departments_employee,
        'department_list': department_list,
        'employee_count': employee_count,
        'employees': employees,
        'total_department': len(Department.objects.all()),
        'total_position': len(Position.objects.all()),
        'total_employee': len(Employees.objects.all()),
    }
    return render(request, 'EmployeeManagement/home.html', context)


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'EmployeeManagement/about.html', context)


# =================================================== Departments ===============================================


def departments(request):
    department_list = Department.objects.all()

    # ================ department  Search ==========================

    if request.GET.get("search"):
        if request.GET.get("searchBox"):
            value = request.GET.get("searchBox")
            department_list = department_list.filter(name__icontains=value)

    # ================== department Report ===========================

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['Department Name', 'Description'])
            instance = department_list
            for department_list in instance:
                writer.writerow([department_list.name, department_list.description])
            response['Content-Disposition'] = 'attachment; filename="Department Report.csv"'
            return response

    context = {
        'page_title': 'Departments',
        'departments': department_list,
    }
    return render(request, 'EmployeeManagement/departments.html', context)


def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()

    context = {
        'department': department
    }
    return render(request, 'EmployeeManagement/manage_department.html', context)


# ========================== Add departments ============================

def save_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:

            # ================== update departments =========================

            save_department = Department.objects.filter(id=data['id']).update(name=data['name'],
                                                                              description=data['description'],
                                                                              status=data['status'])
        else:

            # ================== Add departments =========================

            save_department = Department(name=data['name'], description=data['description'], status=data['status'])
            save_department.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# =============================== delete departments ==========================

def delete_department1(request):
    data = request.POST
    resp = {'status': ''}
    try:
        print(data['id'])
        deletedep = Department.objects.filter(id=data['id'])
        deletedep.delete()
        resp['status'] = 'success'
    except  Exception as e:
        print(e)
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# ==================================================== Positions ===================================================


def positions(request):
    position_list = Position.objects.all()

    # =========================  Position Search =======================

    if request.GET.get("search"):
        if request.GET.get("searchBox"):
            value = request.GET.get("searchBox")
            position_list = position_list.filter(name__icontains=value)

    # ========================= Position Report ======================

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['Position', 'Description'])
            instance = position_list
            for position_list in instance:
                writer.writerow([position_list.name, position_list.description])
            response['Content-Disposition'] = 'attachment; filename="Position Report.csv"'
            return response

    context = {
        'page_title': 'Positions',
        'positions': position_list,
    }
    return render(request, 'EmployeeManagement/positions.html', context)


def manage_positions(request):
    position = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()

    context = {
        'position': position
    }
    return render(request, 'EmployeeManagement/manage_position.html', context)


# ============================== Add positions ===========================

def save_position(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:

            # ================================= update positions =======================

            save_position = Position.objects.filter(id=data['id']).update(name=data['name'],
                                                                          description=data['description'],
                                                                          status=data['status'])
        else:

            # ===================== Add ================================

            save_position = Position(name=data['name'], description=data['description'], status=data['status'])
            save_position.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# ================================ delete positions ============================

def delete_position(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Position.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# =========================================== Employees ========================================================

def employees(request):
    employee_list = Employees.objects.all()

    # ===================== Employee Search ==================

    if request.GET.get("search"):
        if request.GET.get("searchBox"):
            value = request.GET.get("searchBox")
            employee_list = employee_list.filter(code__icontains=value)

    # ===================== Employee Report =======================

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['E-ID', 'Name', 'Department', 'Position'])
            instance = employee_list
            for employee_list in instance:
                writer.writerow(
                    [employee_list.code, employee_list.firstname + employee_list.middlename + employee_list.lastname,
                     employee_list.department_id, employee_list.position_id])
            response['Content-Disposition'] = 'attachment; filename="Employee Report.csv"'
            return response

    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }
    return render(request, 'EmployeeManagement/employees.html', context)


def user(request):
    employee_code = Employees.objects.all().values()
    context = {
        'page_title': 'Employees',
        'employee_code': employee_code,
    }
    return render(request, 'EmployeeManagement/user.html', context)


def employees1(request):
    print(request.POST.get('user_id'))
    print("Fire")

    id = request.POST.get('user_id')
    employee = Employees.objects.filter(code=id)



# ================================ Validation ============================


    if employee:
        employee_list = Employees.objects.filter(id=request.POST.get('user_id'))
    else:
        return HttpResponse("<h1>Invalid</h1>")

    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }
    return render(request, 'EmployeeManagement/employeesView.html', context)


def manage_employees(request):
    employee = {}
    departments = Department.objects.filter(status=1).all()
    positions = Position.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    return render(request, 'EmployeeManagement/manage_employee.html', context)


# =============================== Add employee ========================

def save_employee(request):
    data = request.POST
    resp = {'status': 'failed'}
    if (data['id']).isnumeric() and int(data['id']) > 0:
        check = Employees.objects.exclude(id=data['id']).filter(code=data['code'])
    else:
        check = Employees.objects.filter(code=data['code'])

    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            dept = Department.objects.filter(id=data['department_id']).first()
            pos = Position.objects.filter(id=data['position_id']).first()
            if (data['id']).isnumeric() and int(data['id']) > 0:

                # =============================== update employee ========================================

                save_employee = Employees.objects.filter(id=data['id']).update(code=data['code'],
                                                                               firstname=data['firstname'],
                                                                               middlename=data['middlename'],
                                                                               lastname=data['lastname'],
                                                                               dob=data['dob'], gender=data['gender'],
                                                                               contact=data['contact'],
                                                                               email=data['email'],
                                                                               address=data['address'],
                                                                               department_id=dept, position_id=pos,
                                                                               date_hired=data['date_hired'],
                                                                               salary=data['salary'],
                                                                               status=data['status'])

                # ====================== Add Employee ============================================
            else:
                save_employee = Employees(code=data['code'], firstname=data['firstname'], middlename=data['middlename'],
                                          lastname=data['lastname'], dob=data['dob'], gender=data['gender'],
                                          contact=data['contact'], email=data['email'], address=data['address'],
                                          department_id=dept, position_id=pos, date_hired=data['date_hired'],
                                          salary=data['salary'], status=data['status'])
                save_employee.save()
            resp['status'] = 'success'
        except Exception:
            resp['status'] = 'failed'
            print(Exception)
            print(json.dumps({"code": data['code'], "firstname": data['firstname'], "middlename": data['middlename'],
                              "lastname": data['lastname'], "dob": data['dob'], "gender": data['gender'],
                              "contact": data['contact'], "email": data['email'], "address": data['address'],
                              "department_id": data['department_id'], "position_id": data['position_id'],
                              "date_hired": data['date_hired'], "salary": data['salary'], "status": data['status']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")


# ========================== delete employee ==============================

def delete_employee(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Employees.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except  Exception as e:
        print(e)
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# =========================== view employee =======================

def view_employee(request):
    employee = {}
    departments = Department.objects.filter(status=1).all()
    positions = Position.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    return render(request, 'EmployeeManagement/view_employee.html', context)


# ==================================================== Attendance ===============================================

def saveAttendance(request):
    data = request.POST;
    print(request.POST.get('user_id'))
    print("Fire")
    employee_list = Employees.objects.filter(id=request.POST.get('user_id'))

    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }

    save_attendance = Attendance(eid=data['eid'], date=data['date'], time=data['time'], )
    save_attendance.save()

    return render(request, 'EmployeeManagement/attendance_successfully.html', context)


def attendance(request):
    attendance_List = Attendance.objects.all()

    # =================== Attendance Search ==================

    if request.GET.get("search"):
        if request.GET.get("searchBox"):
            value = request.GET.get("searchBox")
            attendance_List = attendance_List.filter(eid=value)

    # ===================== Attendance Report ==================

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Date', 'Time'])
            instance = attendance_List
            for attendance_List in instance:
                writer.writerow([attendance_List.eid, attendance_List.date, attendance_List.time])
            response['Content-Disposition'] = 'attachment; filename="Attendance Report.csv"'
            return response

    context = {
        'page_title': 'Attendance',
        'att_list': attendance_List,
    }
    return render(request, 'EmployeeManagement/attendance.html', context)


# ===================================================== leave ================================================

def approveleave(request):
    data = request.POST

    leave_list = Leave.objects.all()
    context = {
        'page_title': 'Attendance',
        'leave_list': leave_list,

    }
    saveLeave = Leave.objects.filter(id=request.POST.get('leave_id')).update(status='1', )

    return render(request, 'EmployeeManagement/leave.html', context)


def rejectleave(request):
    data = request.POST;
    leave_list = Leave.objects.all()
    print(request.POST.get('leave_id1'))
    context = {
        'page_title': 'Attendance',
        'leave_list': leave_list,

    }
    saveLeave = Leave.objects.filter(id=request.POST.get('leave_id1')).update(status='2', )

    return render(request, 'EmployeeManagement/leave.html', context)


def leave(request):
    leave_list = Leave.objects.all().order_by('-date')

    # ======================= leave Search ===================

    if request.GET.get("search"):
        if request.GET.get("searchBox"):
            value = request.GET.get("searchBox")
            leave_list = leave_list.filter(eid=value)

    # ======================== leave Report ===============

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['E-ID', 'Leave Type', 'Date', 'Time'])
            instance = leave_list
            for leave_list in instance:
                writer.writerow([leave_list.eid, leave_list.type, leave_list.date, leave_list.time])
            response['Content-Disposition'] = 'attachment; filename="Leave Request Report.csv"'
            return response

    context = {
        'page_title': 'Attendance',
        'leave_list': leave_list,

    }
    return render(request, 'EmployeeManagement/leave.html', context)


@employee_manager_only
def dashboard(request):
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'EmployeeManagement/dashboard.html', context)


def saveLeave(request):
    data = request.POST;
    print(request.POST.get('user_id'))
    print("Fire")
    employee_list = Employees.objects.filter(id=request.POST.get('user_id'))
    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }

    saveLeave = Leave(eid=data['eeid'], date=data['date1'], time=data['time1'], type=data['type'], status='0', )
    saveLeave.save()

    return render(request, 'EmployeeManagement/leave_successfully.html', context)
