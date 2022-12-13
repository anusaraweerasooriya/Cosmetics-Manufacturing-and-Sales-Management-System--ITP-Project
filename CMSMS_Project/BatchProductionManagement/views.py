from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.datetime_safe import datetime, strftime
from FormulationAndLabManagement.models import products, formulation
from WarehouseManagement.models import WarehouseRequest
from .models import *
from .forms import *
from .filters import *
from .decorators import bp_manager_only
import csv
import datetime


@bp_manager_only
def dashboard(request):
    # cards
    pending_batch_req = WarehouseRequest.objects.all().filter(req_from="BP Manager", status="Pending").count()
    pending_material_req = Request.objects.all().filter(status="Pending").count()
    scheduled_productions = ScheduleProduction.objects.all().filter(status="Scheduled").count()
    due_repairs = Machine.objects.all().filter(condition="Need Repair").count()

    # bar chart
    face_makeup = products.objects.filter(product_category='Face Makeup').values('id')
    face_makeup_schedule = ScheduleProduction.objects.filter(product_code__in=face_makeup).values('id')
    face_makeup_batch_count = Batch.objects.filter(schedule_id__in=face_makeup_schedule).count()

    skin_cosmetics = products.objects.filter(product_category='Skin Cosmetics').values('id')
    skin_cosmetics_schedule = ScheduleProduction.objects.filter(product_code__in=skin_cosmetics).values('id')
    skin_cosmetics_batch_count = Batch.objects.filter(schedule_id__in=skin_cosmetics_schedule).count()

    nail_cosmetics = products.objects.filter(product_category='Nail Cosmetics').values('id')
    nail_cosmetics_schedule = ScheduleProduction.objects.filter(product_code__in=nail_cosmetics).values('id')
    nail_cosmetics_batch_count = Batch.objects.filter(schedule_id__in=nail_cosmetics_schedule).count()

    hair_cosmetics = products.objects.filter(product_category='Hair Cosmetics').values('id')
    hair_cosmetics_schedule = ScheduleProduction.objects.filter(product_code__in=hair_cosmetics).values('id')
    hair_cosmetics_batch_count = Batch.objects.filter(schedule_id__in=hair_cosmetics_schedule).count()

    product_category_count = [skin_cosmetics_batch_count, face_makeup_batch_count, nail_cosmetics_batch_count, hair_cosmetics_batch_count]
    product_categories = ['Skin Cosmetics', 'Face Makeup', 'Nail Cosmetics', 'Hair Cosmetics']

    # line chart
    today_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today()).count()
    tomorrow_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today() + datetime.timedelta(days=1)).count()
    day3_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today() + datetime.timedelta(days=2)).count()
    day4_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today() + datetime.timedelta(days=3)).count()
    day5_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today() + datetime.timedelta(days=4)).count()
    day6_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today() + datetime.timedelta(days=5)).count()
    day7_count = ScheduleProduction.objects.filter(due_date__contains=datetime.date.today() + datetime.timedelta(days=6)).count()

    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    day3 = datetime.date.today() + datetime.timedelta(days=2)
    day4 = datetime.date.today() + datetime.timedelta(days=3)
    day5 = datetime.date.today() + datetime.timedelta(days=4)
    day6 = datetime.date.today() + datetime.timedelta(days=5)
    day7 = datetime.date.today() + datetime.timedelta(days=6)

    day_list = [today, tomorrow, day3, day4, day5, day6, day7]
    production_list = [today_count, tomorrow_count, day3_count, day4_count, day5_count, day6_count, day7_count]

    context = {
        'pending_batch_req': pending_batch_req,
        'pending_material_req': pending_material_req,
        'scheduled_productions': scheduled_productions,
        'due_repairs': due_repairs,
        'product_category_count': product_category_count,
        'product_categories': product_categories,
        'day_list': day_list,
        'production_list': production_list,
    }
    return render(request, 'BatchProductionManagement/common/dashboard.html', context)


# View Inventory RawMaterials
@bp_manager_only
def rawmaterials(request):
    rawmaterials = RawMaterial.objects.all().order_by('name')

    all_requests = Request.objects.all().values('rawmaterial')
    all_requested_rm = RawMaterial.objects.filter(id__in=all_requests)
    all_not_requested_rm = RawMaterial.objects.exclude(id__in=all_requests)

    for rm in all_requested_rm:
        rm.deficiency_request = True
        rm.save()

    for rm in all_not_requested_rm:
        rm.deficiency_request = False
        rm.save()

    material_filter = RawMaterialFilter(request.GET, queryset=rawmaterials)
    rawmaterials = material_filter.qs

    context = {
        'rawmaterials': rawmaterials,
        'material_filter': material_filter,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/rawmaterials.html', context)


# Create new Inventory RawMaterial
@bp_manager_only
def createRawmaterial(request):
    rawmaterial_form = RawMaterialForm

    if request.method == 'POST':
        rawmaterial_form = RawMaterialForm(request.POST)
        if rawmaterial_form.is_valid():
            rawmaterial_form.save()
            item = rawmaterial_form.cleaned_data.get('name')
            messages.success(request, item + ' added successfully!')
            return redirect('bp_rawmaterials')

    context = {
        'rawmaterial_form': rawmaterial_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/rawmaterial_form.html', context)


# Update Inventory RawMaterial
@bp_manager_only
def updateRawmaterial(request, pk):
    rawmaterials = RawMaterial.objects.get(id=pk)
    rawmaterial_form = RawMaterialForm(instance=rawmaterials)

    if request.method == 'POST':
        rawmaterial_form = RawMaterialForm(request.POST, instance=rawmaterials)
        if rawmaterial_form.is_valid():
            rawmaterial_form.save()
            item = rawmaterial_form.cleaned_data.get('name')
            messages.success(request, item + ' updated successfully!')
            return redirect('bp_rawmaterials')

    context = {
        'rawmaterial_form': rawmaterial_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/rawmaterial_form.html', context)


# Delete Inventory RawMaterial
@bp_manager_only
def deleteRawmaterial(request, pk):
    rawmaterial = RawMaterial.objects.get(id=pk)

    if request.method == 'POST':
        name = rawmaterial.name
        rawmaterial.delete()
        messages.success(request, name + ' deleted successfully!')
        return redirect('bp_rawmaterials')

    context = {
        'rawmaterial': rawmaterial,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/delete_rawmaterial.html', context)


# View Warehouse Requests sent
@bp_manager_only
def requests(request):
    requests = Request.objects.all().order_by('-last_updated')

    requests_filter = RequestFilter(request.GET, queryset=requests)
    requests = requests_filter.qs

    context = {
        'requests': requests,
        'requests_filter': requests_filter,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/requests.html', context)


# Create new Warehouse Request (from Warehouse Requests page)
@bp_manager_only
def createRequest(request):
    request_form = RequestForm

    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            # Set the RawMaterial -> deficiency_request status to TRUE and save
            messages.success(request, 'Request sent successfully!')
            return redirect('bp_requests')

    context = {
        'request_form': request_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/request_form.html', context)


# Update Warehouse Request sent
@bp_manager_only
def updateRequest(request, pk):
    requests = Request.objects.get(id=pk)
    request_form = RequestForm(instance=requests)

    if request.method == 'POST':
        request_form = RequestForm(request.POST, instance=requests)
        if request_form.is_valid():
            request_form.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('bp_requests')

    context = {
        'request_form': request_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/request_form.html', context)


# Delete Warehouse Request sent
@bp_manager_only
def deleteRequest(request, pk):
    requests = Request.objects.get(id=pk)

    if request.method == 'POST':
        rawmaterial = requests.rawmaterial
        requests.delete()
        messages.success(request, 'Request for ' + rawmaterial.name + ' deleted successfully!')
        return redirect('bp_requests')

    context = {
        'requests': requests,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/delete_request.html', context)


# Confirm Completion of Warehouse request and Update Inventory Raw-Material amount
@bp_manager_only
def requestReceived(request, pk):
    rm_request = Request.objects.get(id=pk)
    rm_request.status = 'Received'
    rm_request.save()
    material = RawMaterial.objects.get(name=rm_request.rawmaterial)
    material.quantity = material.quantity + rm_request.quantity
    material.save()
    messages.success(request, 'Request completed and updated raw-material inventory successfully !')
    return redirect('bp_requests')


# Delete entry after closing the Request
@bp_manager_only
def requestCompletedDelete(request, pk):
    rm_request = Request.objects.get(id=pk)
    rm_request.delete()
    return redirect('bp_requests')


# Create Warehouse request (from Raw-Materials page)
@bp_manager_only
def deficiencyRequest(request, pk):
    rawmaterial = RawMaterial.objects.get(id=pk)
    request_form = RequestForm(initial={'rawmaterial': rawmaterial})

    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            messages.success(request, 'Request for ' + rawmaterial.name + ' sent successfully!')
            return redirect('bp_rawmaterials')

    context = {
        'request_form': request_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/request_form.html', context)


# Render Products from FormulationAndLabManagement
@bp_manager_only
def getProducts(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    f_products = products.objects.filter(
        Q(product_name__icontains=search_query) | Q(product_category__icontains=search_query))

    context = {
        'f_products': f_products,
        'search_query': search_query,
    }
    return render(request, 'BatchProductionManagement/Productions/products.html', context)


# View Product Details
@bp_manager_only
def viewProduct(request, pk):
    f_product = products.objects.get(id=pk)
    f_raw_materials = formulation.objects.filter(product_name=f_product.id)

    scheduled = ScheduleProduction.objects.filter(product_code=f_product, status='Scheduled').count()
    onhold = ScheduleProduction.objects.filter(product_code=f_product, status='On Hold').count()
    completed = ScheduleProduction.objects.filter(product_code=f_product, status='Completed').count()

    now = datetime.date.today()
    current_year = now.year

    product_schedule_ids = ScheduleProduction.objects.filter(product_code=f_product).values('id')
    jan = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=1).count()
    feb = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=2).count()
    mar = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=3).count()
    apr = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=4).count()
    may = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=5).count()
    jun = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=6).count()
    jul = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=7).count()
    aug = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=8).count()
    sep = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=9).count()
    oct = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=10).count()
    nov = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=11).count()
    dec = Batch.objects.filter(schedule_id__in=product_schedule_ids, manufacture_date__year=current_year,
                               manufacture_date__month=12).count()

    context = {
        'f_product': f_product,
        'scheduled': scheduled,
        'onhold': onhold,
        'completed': completed,
        'f_raw_materials': f_raw_materials,
        'current_year': current_year,
        'jan': jan, 'feb': feb, 'mar': mar, 'apr': apr, 'may': may, 'jun': jun,
        'jul': jul, 'aug': aug, 'sep': sep, 'oct': oct, 'nov': nov, 'dec': dec,
    }
    return render(request, 'BatchProductionManagement/Productions/view_product.html', context)


# Access a product and Schedule a Batch Production
@bp_manager_only
def scheduleProduction(request, pk):
    f_product_code = products.objects.get(id=pk)
    schedule_form = ScheduleForm(initial={
        'product_code': f_product_code,
    })

    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            return proceedSchedule(request)
        else:
            return redirect('bp_products')

    context = {
        'schedule_form': schedule_form,
        'f_product_code': f_product_code,
    }
    return render(request, 'BatchProductionManagement/Productions/schedule_form.html', context)


# Check RawMaterials upon Proceeding Schedule (after schedule form submission)
@bp_manager_only
def proceedSchedule(request):
    schedule = ScheduleProduction.objects.all().order_by('-id').first()
    code = schedule.product_code

    f_raw_materials = formulation.objects.filter(product_name=code)
    i_raw_materials = RawMaterial.objects.all()

    context = {
        'schedule': schedule,
        'f_raw_materials': f_raw_materials,
        'i_raw_materials': i_raw_materials,
    }
    return render(request, 'BatchProductionManagement/Productions/proceed_schedule.html', context)


# Create warehouse request (from Proceed Schedule page)
@bp_manager_only
def deficiencyRequestOnSchedule(request, pk, pk2):
    rawmaterial = RawMaterial.objects.get(id=pk)
    request_form = RequestForm(initial={'rawmaterial': rawmaterial, 'quantity': pk2})

    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            rawmaterial.deficiency_request = True
            rawmaterial.save()
            messages.success(request, 'Request for ' + rawmaterial.name + ' sent successfully!')
            return proceedSchedule(request)

    context = {
        'request_form': request_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/request_form.html', context)


@bp_manager_only
def cancelSchedule(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    schedule.delete()
    return redirect('bp_products')


@bp_manager_only
def confirmSchedule(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    schedule.status = 'Scheduled'
    schedule.save()
    messages.success(request, 'Production is scheduled Successfully !')
    return batchProductions(request)


@bp_manager_only
def confirmOnHold(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    schedule.status = 'On Hold'
    schedule.save()
    messages.success(request, 'Production scheduled is OnHold !')
    return batchProductions(request)


# View Scheduled & OnHold Productions
@bp_manager_only
def batchProductions(request):
    bproductions = ScheduleProduction.objects.all()

    now = datetime.date.today()
    current_month = now.month
    monthly_scheduled_list = ScheduleProduction.objects.filter(due_date__month=current_month,
                                                               status='Scheduled').order_by('due_date')
    monthly_onhold_list = ScheduleProduction.objects.filter(due_date__month=current_month, status='On Hold').order_by(
        'due_date')

    scheduled = bproductions.filter(due_date__month=current_month, status='Scheduled').count()
    onhold = bproductions.filter(due_date__month=current_month, status='On Hold').count()
    inprogress = bproductions.filter(due_date__month=current_month, status='In Progress').count()
    completed = bproductions.filter(due_date__month=current_month, status='Completed').count()

    monthly_total = ScheduleProduction.objects.filter(due_date__month=current_month).count()

    context = {
        'bproductions': bproductions,
        'monthly_scheduled_list': monthly_scheduled_list,
        'monthly_onhold_list': monthly_onhold_list,
        'scheduled': scheduled,
        'onhold': onhold,
        'inprogress': inprogress,
        'completed': completed,
        'monthly_total': monthly_total,
    }
    return render(request, 'BatchProductionManagement/Productions/productions.html', context)


@bp_manager_only
def updateProduction(request, pk):
    production = ScheduleProduction.objects.get(id=pk)
    product = production.product_code.id
    f_product_code = products.objects.get(id=product)
    schedule_form = ScheduleForm(instance=production)

    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST, instance=production)
        if schedule_form.is_valid():
            schedule_form.save()
            messages.success(request, 'Scheduled Production updated successfully!')
            return redirect('bp_bproductions')

    context = {
        'schedule_form': schedule_form,
        'f_product_code': f_product_code,
    }
    return render(request, 'BatchProductionManagement/Productions/schedule_form.html', context)


# Delete an onHold production
@bp_manager_only
def deleteProduction(request, pk):
    production = ScheduleProduction.objects.get(id=pk)

    if request.method == 'POST':
        production.delete()
        return redirect('bp_bproductions')

    context = {
        'production': production,
    }
    return render(request, 'BatchProductionManagement/Productions/delete_production.html', context)


# View scheduled production details
@bp_manager_only
def viewScheduled(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    code = schedule.product_code

    f_raw_materials = formulation.objects.filter(product_name=code)
    i_raw_materials = RawMaterial.objects.all()

    context = {
        'schedule': schedule,
        'f_raw_materials': f_raw_materials,
        'i_raw_materials': i_raw_materials,
    }
    return render(request, 'BatchProductionManagement/Productions/view_scheduled.html', context)


# View scheduled production details
@bp_manager_only
def viewOnHold(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    code = schedule.product_code

    f_raw_materials = formulation.objects.filter(product_name=code)
    i_raw_materials = RawMaterial.objects.all()

    context = {
        'schedule': schedule,
        'f_raw_materials': f_raw_materials,
        'i_raw_materials': i_raw_materials,
    }
    return render(request, 'BatchProductionManagement/Productions/view_onhold.html', context)


# Create warehouse request (from On Hold page)
@bp_manager_only
def deficiencyRequestOnHold(request, pk, pk2, pk3):
    rawmaterial = RawMaterial.objects.get(id=pk)
    request_form = RequestForm(initial={'rawmaterial': rawmaterial, 'quantity': pk2})

    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            rawmaterial.deficiency_request = True
            rawmaterial.save()
            messages.success(request, 'Request for ' + rawmaterial.name + ' sent successfully!')
            return viewOnHold(request, pk3)

    context = {
        'request_form': request_form,
    }
    return render(request, 'BatchProductionManagement/Rawmaterials/request_form.html', context)


# Confirm production schedule after raw-materials are available
@bp_manager_only
def confirmScheduleOnHold(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    schedule.status = "Scheduled"
    schedule.save()
    messages.success(request, 'Production is scheduled Successfully !')
    return redirect('bp_bproductions')


# Proceed with a Scheduled Production
@bp_manager_only
def proceedProduction(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    code = schedule.product_code
    f_raw_materials = formulation.objects.filter(product_name=code)
    date = datetime.date.today()
    exp = date + schedule.product_code.duration

    context = {
        'schedule': schedule,
        'date': date,
        'exp': exp,
        'f_raw_materials': f_raw_materials,
    }
    return render(request, 'BatchProductionManagement/Productions/proceed_production.html', context)


# Create a Batch after production is completed
@bp_manager_only
def completeProduction(request, pk):
    schedule = ScheduleProduction.objects.get(id=pk)
    if request.method == 'POST':
        batch_qty = request.POST.get('batch_qty')
        m_date = request.POST.get('m_date')
        e_date = request.POST.get('e_date')
        details = request.POST.get('details')
        batch = Batch(schedule_id=schedule, batch_quantity=batch_qty, manufacture_date=m_date, expiry_date=e_date,
                      batch_details=details)
        batch.save()
        schedule.status = 'Completed'
        schedule.save()
        return render(request, 'BatchProductionManagement/Productions/production_success.html')


# View Batch details
@bp_manager_only
def batches(request):
    batches = Batch.objects.all().order_by('-id')

    face_makeup = products.objects.filter(product_category='Face Makeup').values('id')
    face_makeup_schedule = ScheduleProduction.objects.filter(product_code__in=face_makeup).values('id')
    face_makeup_batch_count = Batch.objects.filter(schedule_id__in=face_makeup_schedule).count()
    face_makeup_ready_batch_count = Batch.objects.filter(schedule_id__in=face_makeup_schedule, status='Ready').count()

    skin_cosmetics = products.objects.filter(product_category='Skin Cosmetics').values('id')
    skin_cosmetics_schedule = ScheduleProduction.objects.filter(product_code__in=skin_cosmetics).values('id')
    skin_cosmetics_batch_count = Batch.objects.filter(schedule_id__in=skin_cosmetics_schedule).count()
    skin_cosmetics_ready_batch_count = Batch.objects.filter(schedule_id__in=skin_cosmetics_schedule,
                                                            status='Ready').count()

    nail_cosmetics = products.objects.filter(product_category='Nail Cosmetics').values('id')
    nail_cosmetics_schedule = ScheduleProduction.objects.filter(product_code__in=nail_cosmetics).values('id')
    nail_cosmetics_batch_count = Batch.objects.filter(schedule_id__in=nail_cosmetics_schedule).count()
    nail_cosmetics_ready_batch_count = Batch.objects.filter(schedule_id__in=nail_cosmetics_schedule,
                                                            status='Ready').count()

    hair_cosmetics = products.objects.filter(product_category='Hair Cosmetics').values('id')
    hair_cosmetics_schedule = ScheduleProduction.objects.filter(product_code__in=hair_cosmetics).values('id')
    hair_cosmetics_batch_count = Batch.objects.filter(schedule_id__in=hair_cosmetics_schedule).count()
    hair_cosmetics_ready_batch_count = Batch.objects.filter(schedule_id__in=hair_cosmetics_schedule,
                                                            status='Ready').count()

    batch_filter = BatchFilter(request.GET, queryset=batches)
    batches = batch_filter.qs

    context = {
        'batches': batches,
        'batch_filter': batch_filter,
        'face_makeup_batch_count': face_makeup_batch_count,
        'face_makeup_ready_batch_count': face_makeup_ready_batch_count,
        'skin_cosmetics_batch_count': skin_cosmetics_batch_count,
        'skin_cosmetics_ready_batch_count': skin_cosmetics_ready_batch_count,
        'nail_cosmetics_batch_count': nail_cosmetics_batch_count,
        'nail_cosmetics_ready_batch_count': nail_cosmetics_ready_batch_count,
        'hair_cosmetics_batch_count': hair_cosmetics_batch_count,
        'hair_cosmetics_ready_batch_count': hair_cosmetics_ready_batch_count,
    }
    return render(request, 'BatchProductionManagement/Batches/batch_details.html', context)


# Update batch status from Ready to Dispatched
@bp_manager_only
def batchDispatch(request, pk):
    batch = Batch.objects.get(id=pk)
    batch.status = 'Dispatched'
    batch.save()
    return redirect('bp_batches')


# View Batch requests from warehouse
@bp_manager_only
def batch_requests(request):
    b_requests = WarehouseRequest.objects.all().filter(req_from="BP Manager")

    context = {
        'b_requests': b_requests,
    }
    return render(request, 'BatchProductionManagement/Batches/batch_requests.html', context)


# View Batch Request Details separately
def view_batch_request(request, pk):
    batch = WarehouseRequest.objects.get(request_ID=pk)
    product = products.objects.filter(product_name=batch.itemName).values('id')
    product_schedules = ScheduleProduction.objects.filter(product_code__in=product).values('id')
    not_dispatched = Batch.objects.filter(schedule_id__in=product_schedules, status='Ready')

    context = {
        'batch': batch,
        'not_dispatched': not_dispatched,
    }
    return render(request, 'BatchProductionManagement/Batches/view_batch_request.html', context)


# Schedule production (from Batch request page)
def schedule_batch_request(request, pk):
    req = WarehouseRequest.objects.get(request_ID=pk)
    product_id = products.objects.get(product_name=req.itemName)
    schedule_form = ScheduleForm(initial={
        'product_code': product_id,
        'target_quantity': req.quantity,
        'due_date': req.due_Date,
    })

    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            req.status = 'Dispatched'
            req.save()
            return proceedSchedule(request)
        else:
            return redirect('bp_products')

    context = {
        'schedule_form': schedule_form,
        'f_product_code': product_id,
    }
    return render(request, 'BatchProductionManagement/Productions/schedule_form.html', context)


# Dispatch and Update batch request status (from Batch request page)
@bp_manager_only
def dispatchBatchRequest(request, pk, pk2):
    batch = Batch.objects.get(id=pk)
    req = WarehouseRequest.objects.get(request_ID=pk2)
    batch.status = 'Dispatched'
    batch.save()
    req.status = 'Accepted'
    req.save()
    return redirect('bp_batch_requests')


# View Machinery
@bp_manager_only
def machinery(request):
    machines = Machine.objects.all()

    context = {
        'machines': machines,
    }
    return render(request, 'BatchProductionManagement/Machinery/machinery.html', context)


# View Machine Details
@bp_manager_only
def view_machinery(request, pk):
    machine = Machine.objects.get(id=pk)

    context = {
        'machine': machine,
    }
    return render(request, 'BatchProductionManagement/Machinery/view_machinery.html', context)


# Add new Machine
@bp_manager_only
def createMachinery(request):
    machinery_form = MachineryForm

    if request.method == 'POST':
        machinery_form = MachineryForm(request.POST, request.FILES)
        if machinery_form.is_valid():
            machinery_form.save()
            item = machinery_form.cleaned_data.get('item_name')
            messages.success(request, item + ' added successfully!')
            return redirect('bp_machinery')

    context = {
        'machinery_form': machinery_form,
    }
    return render(request, 'BatchProductionManagement/Machinery/machinery_form.html', context)


# Update Machine Details
@bp_manager_only
def updateMachinery(request, pk):
    machine = Machine.objects.get(id=pk)
    machinery_form = MachineryForm(instance=machine)

    if request.method == 'POST':
        machinery_form = MachineryForm(request.POST, instance=machine)
        if machinery_form.is_valid():
            machinery_form.save()
            item = machinery_form.cleaned_data.get('item_name')
            messages.success(request, item + ' updated successfully!')
            return redirect('bp_machinery')

    context = {
        'machinery_form': machinery_form,
    }
    return render(request, 'BatchProductionManagement/Machinery/machinery_form.html', context)


@bp_manager_only
def deleteMachinery(request, pk):
    machine = Machine.objects.get(id=pk)

    if request.method == 'POST':
        name = machine.item_name
        machine.delete()
        messages.success(request, name + ' deleted successfully!')
        return redirect('bp_machinery')

    context = {
        'machine': machine,
    }
    return render(request, 'BatchProductionManagement/Machinery/delete_machinery.html', context)


# ----------------------------------REPORT GENERATION------------------------------------------
@bp_manager_only
def materialsCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=RawMaterials_Report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Raw-Material Name', 'Quantity', 'Re-Order Level'])

    materials = RawMaterial.objects.all()
    for material in materials:
        writer.writerow([material.id, material.name, material.quantity, material.reorder_level])
    return response


@bp_manager_only
def requestsCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Requests_Report.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['ID', 'Raw-Material ID', 'Raw-Material Name', 'Quantity', 'Description', 'Date Requested', 'Request Status'])

    requests = Request.objects.all()
    for req in requests:
        writer.writerow(
            [req.id, req.rawmaterial.id, req.rawmaterial.name, req.quantity, req.description, req.date_requested,
             req.status])
    return response


@bp_manager_only
def productionsCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Productions_Report.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['ID', 'Product Code', 'Product Name', 'Target Quantity', 'Net-Weight', 'Due-Date', 'Production Status'])

    productions = ScheduleProduction.objects.all()
    for production in productions:
        writer.writerow(
            [production.id, production.product_code.id, production.product_code, production.target_quantity,
             production.net_weight, production.due_date, production.status])
    return response


@bp_manager_only
def machineryCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Machinery_Report.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['ID', 'Name', 'Model', 'Year', 'Description', 'Power Consumption', 'Net-Weight',
         'Dimensions', 'Date Purchased', 'Repair Duration', 'Last Repair', 'Next Repair', 'Condition'])

    machines = Machine.objects.all()
    for m in machines:
        writer.writerow(
            [m.id, m.item_name, m.model, m.year, m.description, m.power_consumption, m.net_weight,
             m.dimensions, m.date_purchased, m.repair_duration, m.last_repair, m.next_repair, m.condition])
    return response


@bp_manager_only
def batchesCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Batch_Report.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['Batch Number', 'Product Code', 'Product', 'Product Net-Weight',
         'Batch Quantity', 'Manufacture Date', 'Expiry Date', 'Other Details', 'Batch Status'])

    batches = Batch.objects.all()
    for batch in batches:
        writer.writerow(
            [batch.id, batch.schedule_id.product_code.id, batch.schedule_id.product_code, batch.schedule_id.net_weight,
             batch.batch_quantity, batch.manufacture_date, batch.expiry_date, batch.batch_details, batch.status])
    return response


# ----------------------------------HISTORY------------------------------------------
@bp_manager_only
def rawmaterial_history(request):
    materials = RawMaterialHistory.objects.all()

    context = {
        'materials': materials,
    }
    return render(request, 'BatchProductionManagement/History/rawmaterial_history.html', context)


@bp_manager_only
def clear_rawmaterial_history(request):
    material = RawMaterialHistory.objects.all()

    if request.method == 'POST':
        material.delete()
        return redirect('bp_material_history')
    return render(request, 'BatchProductionManagement/History/clear_rawmaterial_history.html')


