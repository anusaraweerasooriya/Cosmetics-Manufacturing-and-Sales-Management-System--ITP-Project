import csv
import os.path
from itertools import chain

import stripe
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import OrderRequestForm, SupplierRegisterForm, SupplierProductForm, CreateNewSupplierForm, SupplierInfoForm, OrderAcceptForm, OrderForm, ReturnForm, S_ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import smanageronly, supplieronly
from django.http import HttpResponse, Http404
from .models import Newsupplier, SupplierProduct, OrderRequest, SupplierInfo, Invoice, Order
from WarehouseManagement.models import WarehouseRequest
from Users.models import Profile
from Users.forms import ProfileUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import JsonResponse
import json


@login_required(login_url='user-login')
@smanageronly
def SM_dashboard(request):
    requests = WarehouseRequest.objects.all().count()
    nsuppliers = Newsupplier.objects.all().count()
    suppliers = User.objects.filter(groups__name='Supplier').count()
    orders = OrderRequest.objects.filter(status='Ordered').count()
    rawmaterials = SupplierInfo.objects.filter(product_category='Raw materials').count()
    packaging = SupplierInfo.objects.filter(product_category='Packaging materials').count()
    equipments = SupplierInfo.objects.filter(product_category='Equipments').count()

    context={
        'orders': orders,
        'suppliers': suppliers,
        'requests': requests,
        'nsuppliers': nsuppliers,
        'rawmaterials': rawmaterials,
        'packaging': packaging,
        'equipments': equipments,
    }
    return render(request, 'SM_dashboard/SM_dashboard.html', context)


@login_required(login_url='user-login')
@supplieronly
def Supplier_dashboard(request):
    items = SupplierProduct.objects.filter(Supplier=request.user).count()
    totitems = SupplierProduct.objects.all().count()
    orders = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='Ordered').filter(order__viewed_status='new').count()
    nrequests = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='Pending').count()
    products = SupplierProduct.objects.filter(Supplier=request.user)
    orderstot = OrderRequest.objects.all()
    orderstot_count = orderstot.count()
    sorders = orderstot.filter(SupplierID__user=request.user).filter(status='Ordered').count()

    context={
        'items': items,
        'totitems': totitems,
        'orders': orders,
        'nrequests': nrequests,
        'products': products,
        'sorders': sorders,
        'orderstot': orderstot,
        'orders_count': orderstot_count,
    }
    return render(request, 'S_dashboard/Supplier_dashboard.html', context)


@login_required(login_url='user-login')
@smanageronly
def Suppliers(request):
    suppliers = User.objects.filter(groups__name='Supplier')
    suppliers_count = suppliers.count()
    rpsuppliers_count = SupplierInfo.objects.filter(product_category='Raw materials').count()
    tepsuppliers_count = SupplierInfo.objects.filter(product_category='Equipments').count()
    pmsuppliers_count = SupplierInfo.objects.filter(product_category='Packaging materials').count()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        suppliers = suppliers.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(supplierinfo__address__icontains=value) | Q(username__icontains=value) | Q(id__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['SupplierID', 'First Name', 'Last Name', 'Email', 'Username'])
            instance = suppliers
            for supplier in instance:
                writer.writerow([supplier.id, supplier.first_name, supplier.last_name,
                                 supplier.email, supplier.username])
            response['Content-Disposition'] = 'attachment; filename="Supplier info.csv"'
            return response

    context = {
        'suppliers': suppliers,
        'suppliers_count': suppliers_count,
        'rpsuppliers_count': rpsuppliers_count,
        'tepsuppliers_count': tepsuppliers_count,
        'pmsuppliers_count': pmsuppliers_count,

    }
    return render(request, 'SM_dashboard/Suppliers.html', context)


@login_required(login_url='user-login')
@smanageronly
def Warehouserequests(request):
    whrequests = WarehouseRequest.objects.all().order_by('-id')
    requests_count = whrequests.count()
    ordered = whrequests.filter(status='Accepted').count()
    notordered = whrequests.filter(status='Pending').count()
    received = whrequests.filter(status='Received').count()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        whrequests = whrequests.filter(
            Q(request_ID__icontains=value) | Q(itemName__icontains=value) | Q(date__icontains=value)
            | Q(status__icontains=value) | Q(type__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['SupplierID', 'First Name', 'Last Name', 'Email', 'Username'])
            instance = whrequests
            for whrequest in instance:
                writer.writerow([whrequest.request_ID, whrequest.type, whrequest.itemName, whrequest.quantity,
                                 whrequest.date, whrequest.due_Date])
            response['Content-Disposition'] = 'attachment; filename="warehouse-requests.csv"'
            return response

    context = {
        'whrequests': whrequests,
        'requests_count': requests_count,
        'ordered': ordered,
        'notordered': notordered,
        'received': received,
    }

    return render(request, 'SM_dashboard/warehouseRequests.html', context)


@login_required(login_url='user-login')
@smanageronly
def RequestOrder(request, pk):
    order = WarehouseRequest.objects.get(id=pk)
    suppliers = User.objects.filter(groups__name='Supplier')

    if request.method == 'POST':
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            form.save()
            order.status = 'Accepted'
            order.save()
            messages.success(request, f'{order} has been ordered.')
            return redirect('SM_dashboard-WarehouseRequests')
    else:
        form = OrderRequestForm(instance=order)

    context = {
        'form': form,
        'Order': order,
        'suppliers': suppliers,
    }
    return render(request, 'SM_dashboard/requestOrder.html', context)


def whrequestview(request, pk):
    order = WarehouseRequest.objects.get(id=pk)
    norder = OrderRequest.objects.get(request_ID=order.request_ID)

    context={
        'order': order,
        'norder': norder,
    }
    return render(request, 'SM_dashboard/view_order.html', context)


@login_required(login_url='user-login')
@smanageronly
def RemoveSupplier(request, pk):
    item = User.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('SM_dashboard-Suppliers')
    context = {
         'item': item,
    }
    return render(request, 'SM_dashboard/RemoveSupplier.html', context)


@login_required(login_url='user-login')
@smanageronly
def ViewSupplier(request, pk):
    item = User.objects.get(id=pk)
    products = SupplierProduct.objects.all()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        products = products.filter(
             Q(Product__icontains=value) | Q(id__icontains=value)
        )

    context = {
        'item': item,
        'products': products,
    }
    return render(request, 'SM_dashboard/view_supplier.html', context)



def SupplierRegistration(request):
    if request.method == 'POST':
        form = SupplierRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,  'Your application has been sent.')
            return redirect('SM_dashboard-SM_dashboard')

    else:
        form = SupplierRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'SM_user/registerForm.html', context)


@login_required(login_url='user-login')
@smanageronly
def newsupplier(request):
    suppliers = Newsupplier.objects.all()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        suppliers = suppliers.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(product_category__icontains=value) | Q(status__icontains=value) | Q(address__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['Firstname', 'Lastname', 'Category', 'Address', 'Status'])
            instance = suppliers
            for supplier in instance:
                writer.writerow([supplier.first_name, supplier.last_name, supplier.product_category,
                                 supplier.address, supplier.status])
            response['Content-Disposition'] = 'attachment; filename="New Suppliers.csv"'
            return response

    context = {
        'suppliers': suppliers,
    }
    return render(request, 'SM_dashboard/NewSuppliers.html', context)


@login_required(login_url='user-login')
@smanageronly
def ViewNewSuppliers(request, pk):
    supplier = Newsupplier.objects.get(id=pk)
    context = {
        'supplier': supplier
    }
    return render(request, 'SM_dashboard/view_newsuppliers.html', context)


@login_required(login_url='user-login')
@smanageronly
def RejectSupplier(request, pk):
    supplier = Newsupplier.objects.get(id=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('SM_dashboard-NewSupplier')
    context = {
         'supplier': supplier,
    }

    return render(request, 'SM_dashboard/RejectSupplier.html', context)


@login_required(login_url='user-login')
@supplieronly
def products(request):
    items = SupplierProduct.objects.all()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        items = items.filter(
            Q(id__icontains=value) | Q(Product__icontains=value)

        )

    if request.method == 'POST':
        form = SupplierProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Supplier = request.user
            instance.save()
            return redirect('S_dashboard-Products')
    else:
        form = SupplierProductForm()

    context = {
        'form': form,
        'items': items,
    }

    return render(request, 'S_dashboard/SupplierProducts.html', context)


@login_required(login_url='user-login')
@supplieronly
def productDelete(request, pk):
    item = SupplierProduct.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('S_dashboard-Products')
    context = {
        'item': item,
    }
    return render(request, 'S_dashboard/Product_delete.html', context)


@login_required(login_url='user-login')
@supplieronly
def productsUpdate(request, pk):
    item = SupplierProduct.objects.get(id=pk)
    if request.method == 'POST':
        form = SupplierProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('S_dashboard-Products')
    else:
        form = SupplierProductForm(instance=item)
    context = {
        'item': item,
        'form': form,
    }
    return render(request, 'S_dashboard/Product_update.html', context)


@login_required(login_url='user-login')
@supplieronly
def smrequests(request):
    orders = OrderRequest.objects.all().order_by('-id')

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        orders = orders.filter(
            Q(itemName__icontains=value) | Q(request_ID__icontains=value) | Q(date__icontains=value) | Q(status__icontains=value)

        )

    context = {
        'orders': orders,
    }
    return render(request, 'S_dashboard/Requests.html', context)


@login_required(login_url='user-login')
@supplieronly
def acceptorder(request, pk):
    order = OrderRequest.objects.get(id=pk)
    init = {
        "request_ID": order,
    }

    if request.method == 'POST':
        form = OrderAcceptForm(request.POST, request.FILES, initial=init)
        if form.is_valid():
            form.save()
            order.status = 'Accepted'
            order.save()
            return redirect('S_dashboard-Requests')
    else:
        form = OrderAcceptForm(initial=init)
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'S_dashboard/Order_accept.html', context)


@login_required(login_url='user-login')
@supplieronly
def rejectorder(request, pk):
    order = OrderRequest.objects.get(id=pk)

    if request.method == 'POST':
        order.status = 'Rejected'
        order.save()
        return redirect('S_dashboard-Requests')

    context = {
        'order': order,
    }
    return render(request, 'S_dashboard/Order_reject.html', context)


@login_required(login_url='user-login')
@supplieronly
def reqOrderView(request, pk):
    order = OrderRequest.objects.get(id=pk)

    context={
        'order': order
    }

    return render(request, 'S_dashboard/view_order_request.html', context)


@login_required(login_url='user-login')
@smanageronly
def AcceptSupplier(request, pk):
    supplier = Newsupplier.objects.get(id=pk)

    if request.method == 'POST':
        Createuserform = CreateNewSupplierForm(request.POST)

        if Createuserform.is_valid():
            user = Createuserform.save()
            supplier.status = 'Accepted'
            supplier.save()

            group = Group.objects.get(name='Supplier')
            user.groups.add(group)

            messages.success(request, f'{supplier} has been added.')
            return redirect('SM_dashboard-NewSupplier')
    else:
        Createuserform = CreateNewSupplierForm(instance=supplier)

    context = {
        'supplier': supplier,
        'Createuserform': Createuserform,
    }
    return render(request, 'SM_dashboard/AcceptSupplier.html', context)


@login_required(login_url='user-login')
@smanageronly
def RemoveNewSupplier(request, pk):
    supplier = Newsupplier.objects.get(id=pk)
    supplier.delete()
    return redirect('SM_dashboard-NewSupplier')


@login_required(login_url='user-login')
@smanageronly
def orderRequests(request):
    orders = OrderRequest.objects.all().order_by('-id')
    order_count = orders.count()
    pending = OrderRequest.objects.filter(status='Pending').count()
    topay = OrderRequest.objects.filter(status='Accepted').count()
    reorder = OrderRequest.objects.filter(status='Rejected').count()+OrderRequest.objects.filter(status='Canceled').count()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        orders = orders.filter(
            Q(request_ID__icontains=value) | Q(itemName__icontains=value) | Q(SupplierID__user__username__icontains=value) |
            Q(date__icontains=value)

        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['RequestID', 'SupplierID', 'Item Name', 'Quantity', 'Price', 'Date', 'Due Date'])
            instance = orders
            for order in instance:
                writer.writerow([order.request_ID, order.SupplierID, order.itemName,
                                 order.quantity, order.invoice.price, order.date, order.due_Date])
            response['Content-Disposition'] = 'attachment; filename="Order Requests info.csv"'
            return response

    context={
        'orders': orders,
        'order_count': order_count,
        'pending': pending,
        'topay': topay,
        'reorder': reorder,
    }
    return render(request, 'SM_dashboard/OrderRequests.html', context)


@login_required(login_url='user-login')
@smanageronly
def pendingrequests(request):
    rorders = OrderRequest.objects.all()
    order_count = rorders.count()
    pending = OrderRequest.objects.filter(status='Pending').count()
    topay = OrderRequest.objects.filter(status='Accepted').count()
    reorder = OrderRequest.objects.filter(status='Rejected').count()+OrderRequest.objects.filter(status='Canceled').count()
    orders = OrderRequest.objects.filter(status='Pending')

    context={
            'orders': orders,
            'order_count': order_count,
            'pending': pending,
            'topay': topay,
            'reorder': reorder,
        }
    return render(request, 'SM_dashboard/OrderRequests.html', context)


@login_required(login_url='user-login')
@smanageronly
def toPay(request):
    rorders = OrderRequest.objects.all()
    order_count = rorders.count()
    pending = OrderRequest.objects.filter(status='Pending').count()
    topay = OrderRequest.objects.filter(status='Accepted').count()
    reorder = OrderRequest.objects.filter(status='Rejected').count()+OrderRequest.objects.filter(status='Canceled').count()
    orders = OrderRequest.objects.filter(status='Accepted')

    context={
            'order_count': order_count,
            'pending': pending,
            'topay': topay,
            'reorder': reorder,
            'orders': orders,
        }
    return render(request, 'SM_dashboard/OrderRequests.html', context)


@login_required(login_url='user-login')
@smanageronly
def to_reorder(request):
    rorders = OrderRequest.objects.all()
    order_count = rorders.count()
    pending = OrderRequest.objects.filter(status='Pending').count()
    topay = OrderRequest.objects.filter(status='Accepted').count()
    reorder = OrderRequest.objects.filter(status='Rejected').count()+OrderRequest.objects.filter(status='Canceled').count()
    reject_orders = OrderRequest.objects.filter(status='Rejected')
    cancel_orders = OrderRequest.objects.filter(status='Canceled')
    orders = list(chain(reject_orders,cancel_orders))

    context = {
        'orders': orders,
        'order_count': order_count,
        'pending': pending,
        'topay': topay,
        'reorder': reorder,
    }
    return render(request, 'SM_dashboard/OrderRequests.html', context)


@login_required(login_url='user-login')
@smanageronly
def Re_Order(request, pk):
    order = OrderRequest.objects.get(id=pk)
    suppliers = User.objects.filter(groups__name='Supplier')

    if request.method == 'POST':
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            form.save()
            order.status = 'Re-ordered'
            order.save()

            messages.success(request, f'{order} has been ordered.')
            return redirect('SM_dashboard-OrderRequests')
    else:
        form = OrderRequestForm(instance=order)

    context = {
        'form': form,
        'Order': order,
        'suppliers': suppliers,
    }
    return render(request, 'SM_dashboard/requestOrder.html', context)


@login_required(login_url='user-login')
@smanageronly
def RemoveRequest(request, pk):
    order = OrderRequest.objects.get(id=pk)
    order.delete()
    return redirect('SM_dashboard-OrderRequests')


@login_required(login_url='user-login')
@smanageronly
def CancelOrder(request, pk):
    order = OrderRequest.objects.get(id=pk)

    if request.method == 'POST':
        order.status = 'Canceled'
        order.save()

        return redirect('SM_dashboard-OrderRequests')

    context={
        'order': order,
    }
    return render(request, 'SM_dashboard/CancelOrder.html', context)


@login_required(login_url='user-login')
@smanageronly
def Invoice(request, pk):
    order = OrderRequest.objects.get(id=pk)

    context = {
        'order': order,
    }
    return render(request, 'SM_dashboard/Invoice_info.html', context)


@login_required(login_url='user-login')
def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response = HttpResponse(fh.read(), content_type="")
            response['Content-Disposition'] = 'inline;filename='+os.path.basename(file_path)
            return response

    raise Http404


@login_required(login_url='user-login')
@smanageronly
def makeOrder(request, pk):
    order = OrderRequest.objects.get(id=pk)
    init = {
        "request_ID": order,
    }

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, initial=init)
        if form.is_valid():
            form.save()
            order.status = 'Ordered'
            order.save()
            return redirect('SM_dashboard-OrderRequests')
    else:
        form = OrderForm(initial=init)

    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'SM_dashboard/MakeOrder.html', context)


@login_required(login_url='user-login')
@supplieronly
def ordersReceived(request):
    orders = OrderRequest.objects.all()
    orders_count = orders.count()
    sorders = orders.filter(SupplierID__user=request.user).filter(status='Ordered').count()
    neworders = orders.filter(SupplierID__user=request.user).filter(status='Ordered').filter(order__viewed_status='new').count()

    context={
        'orders': orders,
        'orders_count': orders_count,
        'neworders': neworders,
        'sorders': sorders,
    }
    return render(request, 'S_dashboard/Myorders.html', context)


@login_required(login_url='user-login')
@supplieronly
def neworders(request):
    myorders = OrderRequest.objects.all()
    orders_count = myorders.count()
    sorders = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='Ordered').count()
    neworders = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='Ordered').filter(order__viewed_status='new').count()
    orders = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='Ordered').filter(order__viewed_status='new')

    context={
        'myorders': myorders,
        'orders_count': orders_count,
        'sorders': sorders,
        'neworders': neworders,
        'orders': orders,
    }
    return render(request, 'S_dashboard/Myorders.html', context)


@login_required(login_url='user-login')
@supplieronly
def orderView(request, pk):
    order = OrderRequest.objects.get(id=pk)

    if request.method == 'POST':
        order.order.viewed_status = 'viewed'
        order.order.save()
        return redirect('S_dashboard-MyOrders')

    context={
        'order': order
    }
    return render(request, 'S_dashboard/Order_view.html', context)


def sm_orderhistory(request):
    orders1 = OrderRequest.objects.filter(status='Ordered')
    orders2 = OrderRequest.objects.filter(status='toreturn')
    orders = list(chain(orders1, orders2))

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['OrderID', 'SupplierID', 'Item Name', 'Quantity', 'Price', 'Ordered Date', 'Due Date'])
            instance = orders
            for order in instance:
                writer.writerow([order.request_ID, order.SupplierID, order.itemName, order.quantity,
                                 order.invoice.price,
                                 order.order.orderedDate, order.due_Date])
            response['Content-Disposition'] = 'attachment; filename="Order history.csv"'
            return response

    context = {
        'orders': orders,
    }
    return render(request, 'SM_dashboard/smOrder_history.html', context)


def markReceived(request, pk):
    order = OrderRequest.objects.get(id=pk)
    order.order.viewed_status = 'received'
    order.order.save()
    return redirect('SM_dashbboard-OrderHistory')



@login_required(login_url='user-login')
@smanageronly
def pendingrequests(request):
    rorders = OrderRequest.objects.all()
    order_count = rorders.count()
    pending = OrderRequest.objects.filter(status='Pending').count()
    topay = OrderRequest.objects.filter(status='Accepted').count()
    reorder = OrderRequest.objects.filter(status='Rejected').count()+OrderRequest.objects.filter(status='Canceled').count()
    orders = OrderRequest.objects.filter(status='Pending')

    context={
            'orders': orders,
            'order_count': order_count,
            'pending': pending,
            'topay': topay,
            'reorder': reorder,
        }
    return render(request, 'SM_dashboard/OrderRequests.html', context)


@login_required(login_url='user-login')
@smanageronly
def orderInfo(request, pk):
    order = OrderRequest.objects.get(id=pk)

    context = {
        'order': order,
    }
    return render(request, 'SM_dashboard/Invoice_info.html', context)


def profile(request):
    product = SupplierProduct.objects.filter(Supplier=request.user).count()
    orders = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='Ordered').count()
    torefund = OrderRequest.objects.filter(SupplierID__user=request.user).filter(status='toreturn').count()

    context={
        'products': product,
        'orders': orders,
        'toreturn': torefund,
    }
    return render(request, 'SM_user/Profile.html', context)


def SprofileUpdate(request):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        S_profile_form = S_ProfileUpdateForm(request.POST, request.FILES, instance=request.user.supplierinfo)

        if user_form.is_valid() and S_profile_form.is_valid():
            user_form.save()
            S_profile_form.save()
            return redirect('SM_user-Profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        S_profile_form = S_ProfileUpdateForm(instance=request.user.supplierinfo)

    context = {
        'user_form': user_form,
        'S_profile_form': S_profile_form,
    }
    return render(request, 'SM_user/EditProfile.html', context)



def SMprofileUpdate(request):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('SM_user-Profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'SM_user/EditProfile.html', context)



@login_required(login_url='user-login')
@smanageronly
def returnRequest(request, pk):
    order = OrderRequest.objects.get(id=pk)
    init = {
        "request_ID": order,
    }

    if request.method == 'POST':
        form = ReturnForm(request.POST, initial=init)
        if form.is_valid():
            form.save()
            order.status = 'toreturn'
            order.save()
            return redirect('SM_dashbboard-OrderHistory')
    else:
        form = ReturnForm(initial=init)

    context = {
        'order': order,
        'form': form,
    }

    return render(request, 'SM_dashboard/ReturnRequest.html', context)


@login_required(login_url='user-login')
@supplieronly
def torefund(request):
    orders = OrderRequest.objects.filter(status='toreturn')

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        orders = orders.filter(
            Q(request_ID__icontains=value) | Q(order__orderedDate__icontains=value) | Q(itemName__icontains=value)
            | Q(returns__refund__icontains=value) | Q(returns__Ship_again__icontains=value)
        )

    context={
        'orders': orders,
    }
    return render(request, 'S_dashboard/toRefund.html', context)


def refund(request, pk):
    order = OrderRequest.objects.get(id=pk)

    if request.method == 'POST':
        order.returns.return_status = 'refunded'
        order.returns.save()
        return redirect('S_dashboard-ToRefund')

    context={
        'order': order,
    }
    return render(request, 'S_dashboard/Refund.html', context)


def paymentsuccess(request, pk):
    order = OrderRequest.objects.get(id=pk)

    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=order.invoice.price,
            currency='lkr',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
    return render(request, 'S_dashboard/Success.html')


def refundeditems(request):
    orders = OrderRequest.objects.filter(returns__return_status='refunded')

    context={
        'orders': orders,
    }
    return render(request, 'S_dashboard/Refundeditems.html', context)


def refundedlist(request):
    orders = OrderRequest.objects.filter(returns__return_status='refunded')

    context={
        'orders': orders,
    }

    return render(request, 'SM_dashboard/SM_refundeditems.html', context)