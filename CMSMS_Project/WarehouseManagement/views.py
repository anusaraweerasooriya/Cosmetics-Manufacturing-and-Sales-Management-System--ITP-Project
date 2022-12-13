from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponse
from django.contrib import messages
from BatchProductionManagement.models import Request, Batch
from EmployeeManagement.models import Employees
from DeliveryManagement.models import Order
from itertools import chain
from datetime import datetime
import csv
from .models import Product, WarehouseRequest, RawMaterial, Equipment, Packaging, WarehouseEmployee, History
from .forms import ProductUpdateForm, WarehouseRequestForm, RawMaterialForm, EquipmentForm, PackagingForm, AcceptEmployeeForm, BatchAcceptForm
from .decorators import whmanageronly, warehousemanager_employeesupervisor, employeesupervisoronly


# Warehouse Manager Dashboard
@login_required(login_url='user-login')
@whmanageronly
def wm_dashboard(request):
    products = Product.objects.all()
    product_count = products.count()
    rawmaterials = RawMaterial.objects.all()
    raw_count = rawmaterials.count()
    pack_count = Packaging.objects.all().count()
    equipment_count = Equipment.objects.all().count()
    batch_count = Request.objects.all().count()

    context = {
        "products": products,
        "product_count": product_count,
        "rawmaterials": rawmaterials,
        "raw_count": raw_count,
        "pack_count": pack_count,
        "equipment_count": equipment_count,
        "batch_count": batch_count,
    }

    return render(request, 'WarehouseManagement/wm_dashboard/index.html', context)


# Employee Supervisor Dashboard
@login_required(login_url='user-login')
@employeesupervisoronly
def es_dashboard(request):
    products_count = Product.objects.all().count()
    orders = Order.objects.all()
    order_count = orders.count()
    not_start = orders.filter(progress='Received').count()
    started = orders.filter(progress='Preparing').count()
    completed = orders.filter(progress='Dispatched').count() + orders.filter(progress='Delivered').count()
    employees = WarehouseEmployee.objects.all()
    employee_count = employees.count()
    not_working = employees.filter(availability='Free').count()
    working = employees.filter(availability='On a Job').count()
    req_count = Request.objects.all().count()

    context = {
        "orders": orders,
        "products_count": products_count,
        "order_count": order_count,
        "employee_count": employee_count,
        "req_count": req_count,
        "not_start": not_start,
        "started": started,
        "completed": completed,
        "not_working": not_working,
        "working": working,
    }

    return render(request, 'WarehouseManagement/es_dashboard/index.html', context)


# View all Products
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_products_view(request):
    products = Product.objects.all()
    products_count = products.values('product').distinct().count()
    category_count = products.values('product').distinct().count()
    reorder_count = products.filter(quantity__lte=F('reorderLevel')).count()
    expire_count = products.filter(product__expiry_date__lte=datetime.now()).count()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        products = products.filter(
            Q(product__schedule_id__product_code__product_name__icontains=value) | Q(product__schedule_id__product_code__product_category__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['Product', 'Quantity', 'Reorder Level'])
            instance = products
            for products in instance:
                writer.writerow([products.product.schedule_id.product_code.product_name, products.quantity,
                                 products.reorderLevel])
            response['Content-Disposition'] = 'attachment; filename="Product Report.csv"'
            return response

    context = {
        "products": products,
        "products_count": products_count,
        "category_count": category_count,
        "reorder_count": reorder_count,
        "expire_count": expire_count,
    }

    return render(request, 'WarehouseManagement/wm_dashboard/products.html', context)


# View Received Batches
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_batch_view(request):
    batches = Batch.objects.all()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        batches = batches.filter(
            Q(schedule_id__product_code__product_name__icontains=value) |
            Q(schedule_id__product_code__product_category__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['Product', 'Category', 'Quantity'])
            instance = batches
            for batches in instance:
                writer.writerow([batches.schedule_id.product_code.product_name, batches.schedule_id.product_code.product_category,
                                 batches.batch_quantity])
            response['Content-Disposition'] = 'attachment; filename="Received Batches Report.csv"'
            return response

    context = {
        "batches": batches,
    }

    return render(request, 'WarehouseManagement/wm_dashboard/batchreceived.html', context)


# Batch product accept
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_batch_status_change(request, pk):
    batch = Batch.objects.get(id=pk)
    init = {
        'product': batch,
        'quantity': batch.batch_quantity,
    }
    if request.method == 'POST':
        form = BatchAcceptForm(request.POST)
        if form.is_valid():
            batch.status = 'Received'
            batch.save()
            form.save()
            return redirect('wm-batch-received')
    else:
        form = BatchAcceptForm(initial=init)

    context = {
        "form": form,
    }

    return render(request, 'WarehouseManagement/wm_dashboard/acceptbatch.html', context)


# View Product Details
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_product_details(request, pk):
    products = Product.objects.get(id=pk)

    context = {
        "products": products,
    }

    return render(request, 'WarehouseManagement/wm_dashboard/productdetails.html', context)


# Product Update
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_product_update(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('wm-products')
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        "form": form,
    }

    return render(request, 'WarehouseManagement/wm_dashboard/productupdate.html', context)


# Product Delete
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_product_delete(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('wm-products')

    context = {
        "title": "Product",
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)


# Reorder Product
@login_required(login_url='user-login')
@whmanageronly
def wm_product_reorder(request, pk):
    product = Product.objects.get(id=pk)
    init = {
        "itemName": product.product.schedule_id.product_code.product_name
    }
    if request.method == 'POST':
        form = WarehouseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wm-products')
    else:
        form = WarehouseRequestForm(instance=product, initial=init)

    context = {
        "form": form,
        "header": "Products",
        "name": product.product.schedule_id.product_code.product_name,
    }

    return render(request, 'WarehouseManagement/common/reorder.html', context)


# Reorder form
@login_required(login_url='user-login')
@whmanageronly
def wm_reorder(request):
    if request.method == 'POST':
        form = WarehouseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wm-dashboard')
    else:
        form = WarehouseRequestForm()

    context = {
        "form": form,
        "header": "",
    }

    return render(request, 'WarehouseManagement/common/reorder.html', context)


# View Requests to Supplier Manager
@login_required(login_url='user-login')
@whmanageronly
def wm_request_supplier(request):
    wh_requests = WarehouseRequest.objects.filter(req_from="Supplier Manager")

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        wh_requests = wh_requests.filter(
            Q(itemName__icontains=value) | Q(type__icontains=value) | Q(status__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Item Name', 'Quantity(kg)', 'Date', 'Due Date'])
            instance = wh_requests
            for wh_request in instance:
                writer.writerow([wh_request.request_ID, wh_request.itemName, wh_request.quantity,
                                 wh_request.date, wh_request.due_Date])
            response['Content-Disposition'] = 'attachment; filename="Orders to Suppliers Report.csv"'
            return response

    context = {
        "wh_requests": wh_requests,
        "title": "Supplier Requests",
        "breadcrumb": "Supplier",
    }

    return render(request, 'WarehouseManagement/common/warehouserequests.html', context)


# View Requests to Batch Production Manager
@login_required(login_url='user-login')
@whmanageronly
def wm_request_batch(request):
    wh_requests = WarehouseRequest.objects.filter(req_from="BP Manager")

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        wh_requests = wh_requests.filter(
            Q(itemName__icontains=value) | Q(type__icontains=value) | Q(status__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Product', 'Quantity', 'Date', 'Due Date'])
            instance = wh_requests
            for wh_request in instance:
                writer.writerow([wh_request.request_ID, wh_request.itemName, wh_request.quantity,
                                 wh_request.date, wh_request.due_Date])
            response['Content-Disposition'] = 'attachment; filename="Orders to Batch Production Report.csv"'
            return response

    context = {
        "wh_requests": wh_requests,
        "title": "Batch  Requests",
        "breadcrumb": "Batch  Production",
    }

    return render(request, 'WarehouseManagement/common/warehouserequests.html', context)


# Update Warehouse Request
@login_required(login_url='user-login')
@whmanageronly
def wm_request_update(request, pk):
    wh_request = WarehouseRequest.objects.get(id=pk)
    if request.method == 'POST':
        form = WarehouseRequestForm(request.POST, instance=wh_request)
        if form.is_valid():
            form.save()
            if wh_request.req_from == "Supplier Manager":
                return redirect('wm-requests-supplier')
            else:
                return redirect('wm-requests-batch')
    else:
        form = WarehouseRequestForm(instance=wh_request)

    context = {
        "form": form,
        "header": "Request",
    }

    return render(request, 'WarehouseManagement/common/update.html', context)


# delete Warehouse Request
@login_required(login_url='user-login')
@whmanageronly
def wm_request_delete(request, pk):
    wh_request = WarehouseRequest.objects.get(id=pk)
    if request.method == 'POST':
        wh_request.delete()
        if wh_request.req_from == "Supplier Manager":
            return redirect('wm-requests-supplier')
        else:
            return redirect('wm-requests-batch')

    context = {
        "title": "Request",
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)


# View Inventory
@login_required(login_url='user-login')
@whmanageronly
def wm_inventory(request):
    materials = RawMaterial.objects.all()
    packagings = Packaging.objects.all()
    equipments = Equipment.objects.all()
    materials_count = materials.count()
    packagings_count = packagings.count()
    equipments_count = equipments.count()

    items = list(chain(materials, packagings, equipments))

    if request.GET.get("search"):
        if request.GET.get('search_field'):
            value = request.GET.get('search_field')
            a = materials.filter(Q(itemName__icontains=value) | Q(category__icontains=value))
            b = packagings.filter(Q(itemName__icontains=value) | Q(category__icontains=value))
            c = equipments.filter(Q(itemName__icontains=value) | Q(category__icontains=value))
            items = list(chain(a, b, c))

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Raw Material', 'Category', 'In Stock'])
            instance = items
            for item in instance:
                writer.writerow([item.itemID, item.itemName, item.category, item.quantity])
            response['Content-Disposition'] = 'attachment; filename="Inventory Report.csv"'
            return response

    context = {
        "materials": materials,
        "packagings": packagings,
        "equipments": equipments,
        "items": items,
        "materials_count": materials_count,
        "packagings_count": packagings_count,
        "equipments_count": equipments_count,
    }

    return render(request, 'WarehouseManagement/inventory/inventory.html', context)


# View and Add Raw Materials
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_rawmaterials(request):
    rawmaterials = RawMaterial.objects.all()
    material_count = rawmaterials.values('itemName').distinct().count()
    category_count = rawmaterials.values('category').distinct().count()
    reorder_count = rawmaterials.filter(quantity__lte=F('reorderLevel')).count()
    expire_count = rawmaterials.filter(expireDate__lte=datetime.now()).count()

    if request.method == 'POST':
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Raw Material Added Successfully')
            return redirect('wm-raw-materials')
    else:
        form = RawMaterialForm()

    if request.GET.get("search"):
        if request.GET.get('search_field'):
            value = request.GET.get('search_field')
            rawmaterials = rawmaterials.filter(
                Q(itemName__icontains=value) | Q(category__icontains=value)
            )
    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Raw Material', 'Category', 'In Stock(kg)', 'Expire Date'])
            instance = rawmaterials
            for rawmaterial in instance:
                writer.writerow([rawmaterial.itemID, rawmaterial.itemName, rawmaterial.category, rawmaterial.quantity, rawmaterial.expireDate])
            response['Content-Disposition'] = 'attachment; filename="Raw Material Report.csv"'
            return response

    context = {
        "rawmaterials": rawmaterials,
        "form": form,
        "material_count": material_count,
        "category_count": category_count,
        "reorder_count": reorder_count,
        "expire_count": expire_count,
    }

    return render(request, 'WarehouseManagement/inventory/rawmaterials.html', context)


# View details of Raw Material
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_rawmaterial_details(request, pk):
    material = RawMaterial.objects.get(id=pk)

    context = {
        "material": material,
        "item": material.itemName,
    }

    return render(request, 'WarehouseManagement/inventory/rawmaterialdetails.html', context)


# update a Raw Material
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_rawmaterial_update(request, pk):
    rawmaterial = RawMaterial.objects.get(id=pk)
    if request.method == 'POST':
        form = RawMaterialForm(request.POST, instance=rawmaterial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Raw Material Updated Successfully')
            return redirect('wm-raw-materials')
    else:
        form = RawMaterialForm(instance=rawmaterial)

    context = {
        "form": form,
        "header": "Raw Material",
    }

    return render(request, 'WarehouseManagement/common/update.html', context)


# Delete a Raw Material
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_rawmaterial_delete(request, pk):
    rawmaterial = RawMaterial.objects.get(id=pk)
    title = rawmaterial.itemName
    if request.method == 'POST':
        rawmaterial.delete()
        messages.error(request, 'Raw Material Deleted Successfully')
        return redirect('wm-raw-materials')

    context = {
        "title": title,
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)


# Raw Material Reorder
@login_required(login_url='user-login')
@whmanageronly
def wm_rawmaterial_reorder(request, pk):
    material = RawMaterial.objects.get(id=pk)
    if request.method == 'POST':
        form = WarehouseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Re-Ordered Successfully')
            return redirect('wm-raw-materials')
    else:
        form = WarehouseRequestForm(instance=material)

    context = {
        "form": form,
        "header": "Raw Materials",
        "name": material.itemName,
    }

    return render(request, 'WarehouseManagement/common/reorder.html', context)


# View and Add Equipments
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_equipments(request):
    equipments = Equipment.objects.all()
    item_count = equipments.values('itemName').distinct().count()
    category_count = equipments.values('category').distinct().count()
    maintain_count = equipments.filter(nextMaintenanceDate__lte=datetime.now()).count()
    fair_count = equipments.filter(status='Fair').count()
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Equipment Added Successfully')
            return redirect('wm-equipments')
    else:
        form = EquipmentForm()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        equipments = equipments.filter(
            Q(itemName__icontains=value) | Q(category__icontains=value) | Q(status__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Equipment', 'Category', 'Quantity', 'Status', 'Last Maintenance Date', 'Next Maintenance Date'])
            instance = equipments
            for equipment in instance:
                writer.writerow([equipment.itemID, equipment.itemName, equipment.category, equipment.quantity,
                                 equipment.status, equipment.lastMaintenanceDate, equipment.nextMaintenanceDate])
            response['Content-Disposition'] = 'attachment; filename="Equipment Status Report.csv"'
            return response

    context = {
        'equipments': equipments,
        'form': form,
        "item_count": item_count,
        "category_count": category_count,
        "maintain_count": maintain_count,
        "fair_count": fair_count,
    }

    return render(request, 'WarehouseManagement/inventory/equipments.html', context)


# View Details of an Equipment
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_equipment_details(request, pk):
    material = Equipment.objects.get(id=pk)

    context = {
        "material": material,
        "item": material.itemName,
    }

    return render(request, 'WarehouseManagement/inventory/equipmentdetails.html', context)


# Update an Equipment
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_equipment_update(request, pk):
    material = Equipment.objects.get(id=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment Updated Successfully')
            return redirect('wm-equipments')
    else:
        form = EquipmentForm(instance=material)

    context = {
        "form": form,
        "header": material.itemName,
    }

    return render(request, 'WarehouseManagement/common/update.html', context)


# Delete an Equipment
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_equipment_delete(request, pk):
    material = Equipment.objects.get(id=pk)
    if request.method == 'POST':
        material.delete()
        messages.error(request, 'Equipment Deleted Successfully')
        return redirect('wm-equipments')

    context = {
        "title": material.itemName,
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)


# View and Add Packaging
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_packaging(request):
    packagings = Packaging.objects.all()
    item_count = packagings.values('itemName').distinct().count()
    category_count = packagings.values('materialType').distinct().count()
    reorder_count = packagings.filter(quantity__lte=F('reorderLevel')).count()

    if request.method == 'POST':
        form = PackagingForm(request.POST)
        form.save()
        messages.info(request, 'Packaging Added Successfully')
        return redirect('wm-packaging')
    else:
        form = PackagingForm()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        packagings = packagings.filter(
            Q(itemName__icontains=value) | Q(category__icontains=value) | Q(materialType__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Packaging', 'Category', 'Material Type', 'In Stock'])
            instance = packagings
            for packaging in instance:
                writer.writerow([packaging.itemID, packaging.itemName, packaging.category, packaging.materialType, packaging.quantity])
            response['Content-Disposition'] = 'attachment; filename="Packaging Report.csv"'
            return response

    context = {
        "packagings": packagings,
        "form": form,
        "item_count": item_count,
        "category_count": category_count,
        "reorder_count": reorder_count,
    }

    return render(request, 'WarehouseManagement/inventory/packaging.html', context)


# View Details of a Packaging Item
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_packaging_details(request, pk):
    packaging = Packaging.objects.get(id=pk)

    context = {
        "packaging": packaging,
        "item": packaging.itemName,
    }

    return render(request, 'WarehouseManagement/inventory/packagingdetails.html', context)


# Update Details of a Packaging Item
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_packaging_update(request, pk):
    packaging = Packaging.objects.get(id=pk)
    if request.method == 'POST':
        form = PackagingForm(request.POST, instance=packaging)
        if form.is_valid():
            form.save()
            messages.success(request, 'Packaging Updated Successfully')
            return redirect('wm-packaging')
    else:
        form = PackagingForm(instance=packaging)

    context = {
        "form": form,
        "header": packaging.itemName,
    }

    return render(request, 'WarehouseManagement/common/update.html', context)


# Delete a Packaging Detail
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_packaging_delete(request, pk):
    packaging = Packaging.objects.get(id=pk)
    if request.method == 'POST':
        packaging.delete()
        messages.error(request, 'Packaging Deleted Successfully')
        return redirect('wm-packaging')

    context = {
        "title": packaging.itemName,
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)


# Packaging Reorder
@login_required(login_url='user-login')
@whmanageronly
def wm_packaging_reorder(request, pk):
    packaging = Packaging.objects.get(id=pk)
    if request.method == 'POST':
        form = WarehouseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Packaging Re-Ordered Successfully')
            return redirect('wm-raw-materials')
    else:
        form = WarehouseRequestForm(instance=packaging)

    context = {
        "form": form,
        "header": "Packagings",
        "name": packaging.itemName,
    }

    return render(request, 'WarehouseManagement/common/reorder.html', context)


# View Requests from Batch Production
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_request_from_batch(request):
    bprequests = Request.objects.all()

    if request.GET.get('search_field'):
        value = request.GET.get('search_field')
        bprequests = bprequests.filter(
            Q(rawmaterial__name__icontains=value) | Q(status__icontains=value)
        )

    if request.method == 'GET':
        click = request.GET.get("export")
        if click:
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            writer.writerow(['ID', 'Raw Material', 'Quantity(kg)', 'Date', 'Status'])
            instance = bprequests
            for bprequest in instance:
                writer.writerow([bprequest.id, bprequest.rawmaterial.name, bprequest.quantity,
                                 bprequest.date_requested, bprequest.status])
            response['Content-Disposition'] = 'attachment; filename="Orders From Batch Production Report.csv"'
            return response

    context = {
        "bprequests": bprequests,
        "title": "Requests from Factory"
    }

    return render(request, 'WarehouseManagement/wm_dashboard/batchrequests.html', context)


# Update Request status from batch Production
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_request_batch_status_update(request, pk):
    bprequest = Request.objects.get(id=pk)
    rawmaterial = RawMaterial.objects.get(itemName=bprequest.rawmaterial.name)
    if rawmaterial:
        if rawmaterial.quantity > bprequest.quantity:
            bprequest.status = 'Completed'
            bprequest.save()
            rawmaterial.quantity = rawmaterial.quantity - bprequest.quantity
            rawmaterial.save()
            return redirect('wm-requests-from-batch')
        else:
            return HttpResponse('<h1>Not enough materials</h1>')
    else:
        return HttpResponse('<h1>Raw Material Not Found</h1>')


# View all Orders
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_orders(request):
    orders = Order.objects.all()
    tot_orders = orders.count()
    not_started = orders.filter(progress='Received').count()
    on_going = orders.filter(progress='Preparing').count()
    completed = orders.filter(progress='Dispatched').count() + orders.filter(progress='Delivered').count()

    context = {
        "orders": orders,
        "not_started": not_started,
        "on_going": on_going,
        "completed": completed,
        "tot_orders": tot_orders,
    }

    return render(request, 'WarehouseManagement/works/orders.html', context)


# Change Order progress
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_order_start(request, pk):
    order = Order.objects.get(id=pk)
    order.progress = 'Preparing'
    order.save()
    return redirect('wm-orders')


# Change Order progress
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_order_complete(request, pk):
    order = Order.objects.get(id=pk)
    order.progress = 'Dispatched'
    order.save()
    return redirect('wm-orders')


# Change Order progress
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_order_finish(request, pk):
    order = Order.objects.get(id=pk)
    order.progress = 'Delivered'
    order.save()
    return redirect('wm-orders')


# Change Order progress
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_order_reset(request, pk):
    order = Order.objects.get(id=pk)
    order.progress = 'Received'
    order.save()
    return redirect('wm-orders')


# Remove an Order
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_order_remove(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        messages.error(request, 'Order Deleted Successfully')
        return redirect('wm-orders')

    context = {}

    return render(request, 'WarehouseManagement/common/delete.html', context)


# View Employees
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employees(request):
    employees = Employees.objects.filter(department_id__name='Warehouse')
    labours = WarehouseEmployee.objects.all()
    employees_count = labours.count()
    new_count = employees.filter(status='Pending').count()
    free_count = labours.filter(availability='Free').count()
    working_count = employees_count - free_count

    context = {
        "employees": employees,
        "labours": labours,
        "employees_count": employees_count,
        "new_count": new_count,
        "free_count": free_count,
        "working_count": working_count,
    }

    return render(request, 'WarehouseManagement/works/employees.html', context)


# Accept New Employees
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_accept(request, pk):
    employee = Employees.objects.get(id=pk)
    init = {
        'employee': employee,
    }
    if request.method == 'POST':
        form = AcceptEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            employee.status = 0
            employee.save()
            messages.info(request, 'Employee Accepted !')
            return redirect('wm-employees')
    else:
        form = AcceptEmployeeForm(initial=init)

    context = {
        "form": form,
        "employee": employee,
    }

    return render(request, 'WarehouseManagement/works/acceptemployee.html', context)


# View details of new employees
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_new_view(request, pk):
    employee = Employees.objects.get(id=pk)

    context = {
        "employee": employee,
    }

    return render(request, 'WarehouseManagement/works/viewemployee.html', context)


# View details of currently working employees
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_view(request, pk):
    employee = WarehouseEmployee.objects.get(id=pk)

    context = {
        "employee": employee,
    }

    return render(request, 'WarehouseManagement/works/viewworkingemployee.html', context)


# Update Employee working sector
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_update(request, pk):
    employee = WarehouseEmployee.objects.get(id=pk)
    if request.method == 'POST':
        form = AcceptEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee Updated Successfully')
            return redirect('wm-employees')
    else:
        form = AcceptEmployeeForm(instance=employee)

    context = {
        "form": form,
        "header": "Employee",
    }

    return render(request, 'WarehouseManagement/common/update.html', context)


# Remove Employees
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_remove(request, pk):
    employee = WarehouseEmployee.objects.get(id=pk)
    if request.method == 'POST':
        employee.delete()
        messages.error(request, 'Employee Removed..')
        return redirect('wm-employees')

    context = {
        "title": "Employee",
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)


# Change Employee Availability
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_assign(request, pk):
    employee = WarehouseEmployee.objects.get(id=pk)
    employee.availability = 'On a Job'
    employee.save()
    return redirect('wm-employees')


# Change Employee Availability
@login_required(login_url='user-login')
@warehousemanager_employeesupervisor
def wm_employee_free(request, pk):
    employee = WarehouseEmployee.objects.get(id=pk)
    employee.availability = 'Free'
    employee.save()
    return redirect('wm-employees')


# View History
@login_required(login_url='user-login')
@whmanageronly
def wm_history(request):
    records = History.objects.all().order_by('-id').values()

    context = {
        "records": records,
    }

    return render(request, 'WarehouseManagement/works/history.html', context)


# Clear History
@login_required(login_url='user-login')
@whmanageronly
def wm_history_clear(request):
    history = History.objects.all()
    if request.method == 'POST':
        history.delete()
        return redirect('wm-history')

    context = {
        "title": "History",
    }

    return render(request, 'WarehouseManagement/common/delete.html', context)
