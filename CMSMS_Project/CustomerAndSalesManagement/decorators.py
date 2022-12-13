from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('customer_products')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to access this content')

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function


def sales_manager_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'SalesManager':
            return view_func(request, *args, **kwargs)
        if group == 'SupplierManager':
            return redirect('SM_dashboard-SM_dashboard')
        if group == 'Supplier':
            return redirect('S_dashboard-Supplier_dashboard')
        if group == 'EmployeeSupervisor':
            return redirect('es-dashboard')
        if group == 'customer':
            return redirect('')
        if group == 'WarehouseManager':
            return redirect('wm-dashboard')
        if group == 'BatchProductionManager':
            return redirect('bp_dashboard')
        if group == 'LaboratoryManager':
            return redirect('FL_dashboard')
        if group == 'DeliveryManager':
            return redirect('DM_dashboard')
        if group == 'EmployeeManager':
            return redirect('dashboard')
        if group == 'CostAnalysisManager':
            return redirect('CA_dashboard')

    return wrapper_func

