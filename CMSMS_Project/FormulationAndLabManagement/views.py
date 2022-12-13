from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
import datetime
from django.http import HttpResponse
import csv
# Create your views here.


def FL_dashboard(request):
    productcount = products.objects.all().count()
    testscount = schedule_test.objects.all().count()
    equipmentscount = equipments.objects.all().count()
    chemicalscount = test_chemicals.objects.all().count()

    haircount = products.objects.filter(product_category='Hair Cosmetics').count()
    skincount = products.objects.filter(product_category='Skin Cosmetics').count()
    nailcount = products.objects.filter(product_category='Nail Cosmetics').count()
    makeupcount = products.objects.filter(product_category='Face Makeup').count()

    successcount = schedule_test.objects.filter(status='Success').count()
    unsuccessscount = schedule_test.objects.filter(status='Unsuccess').count()
    pendingcount = schedule_test.objects.filter(status='Pending').count()

    categorylist = ['Hair Cosmetics', 'Skin Cosmetics', 'Nail Cosmetics', 'Face Makeup']
    categorycount = [haircount, skincount, nailcount, makeupcount]

    statuslist = ['Success', 'Pending', 'Unsuccess']
    statuscountlist = [successcount, unsuccessscount, pendingcount]

    product = products.objects.all()

    context = {
        'productcount': productcount,
        'testscount':testscount,
        'equipmentscount': equipmentscount,
        'chemicalscount': chemicalscount,
        'categorylist': categorylist,
        'categorycount': categorycount,
        'product': product,
        'statuslist':statuslist,
        'statuscountlist':statuscountlist,
    }
    return render(request, 'FormulationAndLabManagement/base/index.html', context)

def FL_productsdashboard(request):
    haircount = products.objects.filter(product_category='Hair Cosmetics').count()
    skincount = products.objects.filter(product_category='Skin Cosmetics').count()
    nailcount = products.objects.filter(product_category='Nail Cosmetics').count()
    makeupcount = products.objects.filter(product_category='Face Makeup').count()

    categorylist = ['Hair Cosmetics', 'Skin Cosmetics', 'Nail Cosmetics', 'Face Makeup']
    categorycount = [haircount, skincount, nailcount, makeupcount]

    context = {
        'categorylist': categorylist,
        'categorycount': categorycount,
    }
    return render(request, 'FormulationAndLabManagement/products/products_dashboard.html', context)

def FL_products(request):
    product = products.objects.all()

    productFilter = ProductsFilter(request.GET, queryset=product)
    product = productFilter.qs

    context = {'product': product, 'productFilter': productFilter}
    return render(request, 'FormulationAndLabManagement/products/products.html', context)

def FL_filteredproducts(request):
    product = products.objects.all()
    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/filtered_products.html', context)

def FL_productprofile(request, pk_product):
    product = products.objects.get(id=pk_product)
    formulations = product.formulation_set.all()
    context = {'product': product, 'formulations': formulations}
    return render(request, 'FormulationAndLabManagement/products/product_profile.html', context)

def FL_addproducts(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/formulation/products/')

    context = {'form': form}
    return render(request, 'FormulationAndLabManagement/products/add_product.html', context)


def FL_updateproduct(request, pk_product):
    product = products.objects.get(id=pk_product)
    form = AddProductForm(instance=product)

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/formulation/products/')

    context = {'form': form}
    return render(request, 'FormulationAndLabManagement/products/update_product.html', context)

def FL_deleteproduct(request, pk_product):
    product = products.objects.get(id=pk_product)

    if request.method == 'POST':
        product.delete()
        return redirect('/formulation/products/')

    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/delete_product.html', context)

def FL_deleteproducthistory(request):
    product = products_history.objects.all()

    if request.method == 'POST':
        product.delete()
        return redirect('/formulation/producthistory/')

    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/delete_history.html', context)

def FL_filterskincosmetics(request):
    product = products.objects.filter(product_category='Skin Cosmetics')
    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/filtered_products.html', context)

def FL_filterhaircosmetics(request):
    product = products.objects.filter(product_category='Hair Cosmetics')
    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/filtered_products.html', context)

def FL_filternailcosmetics(request):
    product = products.objects.filter(product_category='Nail Cosmetics')
    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/filtered_products.html', context)

def FL_filterfacemakeup(request):
    product = products.objects.filter(product_category='Face Makeup')
    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/filtered_products.html', context)



def FL_formulation(request, pk_product):
    FormulationFormSet = inlineformset_factory(products, formulation, fields=('raw_material', 'formulation_qty'), can_delete=False, extra=8)
    product = products.objects.get(id=pk_product)
    id = product.id
    formset = FormulationFormSet(queryset=formulation.objects.none(), instance=product)
    if request.method == 'POST':
        formset = FormulationFormSet(request.POST, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect('/formulation/products/')

    context = {'formset':formset, 'product':product}
    return render(request, 'FormulationAndLabManagement/formulation/formulation.html', context)

def FL_editformulation(request, pk_product):
    FormulationFormSet = inlineformset_factory(products, formulation, fields=('raw_material', 'formulation_qty'), extra=0)
    product = products.objects.get(id=pk_product)
    formset = FormulationFormSet(instance=product)
    if request.method == 'POST':
        formset = FormulationFormSet(request.POST, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect('/formulation/products/')

    context = {'formset': formset, 'product': product}
    return render(request, 'FormulationAndLabManagement/formulation/formulation.html', context)



def FL_equipments(request):
    equipment = equipments.objects.all()
    testtube_count = equipment.filter(category='Test Tube').count()
    flask_count = equipment.filter(category='Flask').count()
    beaker_count = equipment.filter(category='Beaker').count()
    pipette_count = equipment.filter(category='Pipette').count()
    burette_count = equipment.filter(category='Burette').count()
    cylinder_count = equipment.filter(category='Measuring Cylinder').count()
    stand_count = equipment.filter(category='Laboratory Stand').count()
    funnel_count = equipment.filter(category='Funnel').count()

    usedcount = equipment.filter(condition='Used').count()
    brandnewcount = equipment.filter(condition='Brand New').count()
    repaircount = equipment.filter(condition='Need Repair').count()

    countlist = [usedcount, brandnewcount, repaircount]
    conditionlist = ['Used', 'Brand New', 'Need Repair']

    equipmentlist = ['Test Tube', 'Flask', 'Beaker', 'Pipette', 'Burette', 'Measuring Cylinder', 'Laboratory Stand', 'Funnel']
    equipmentcount = [testtube_count, flask_count, beaker_count, pipette_count, burette_count, cylinder_count, stand_count, funnel_count]

    context={
        'testtube_count': testtube_count,
        'flask_count': flask_count,
        'beaker_count': beaker_count,
        'pipette_count': pipette_count,
        'burette_count': burette_count,
        'cylinder_count': cylinder_count,
        'stand_count': stand_count,
        'funnel_count': funnel_count,
        'equipmentlist': equipmentlist,
        'equipmentcount': equipmentcount,
        'countlist': countlist,
        'conditionlist': conditionlist,
    }
    return render(request, 'FormulationAndLabManagement/equipments/equipments.html', context)

def FL_equipmentlist(request):
    equipment = equipments.objects.all()

    equipmentFilter = EquipmentsFilter(request.GET, queryset=equipment)
    equipment = equipmentFilter.qs

    context = {'equipment': equipment, 'equipmentFilter': equipmentFilter}
    return render(request, 'FormulationAndLabManagement/equipments/equipment_list.html', context)

def FL_filteredequipments(request):
    equipment = equipments.objects.all()
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/products/filtered_equipments.html', context)

def FL_addequipments(request):
    form = AddEquipmentForm()
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/formulation/equipmentlist/')

    context = {'form': form}
    return render(request, 'FormulationAndLabManagement/equipments/add_equipment.html', context)

def FL_updateequipment(request, pk_equipment):
    equipment = equipments.objects.get(id=pk_equipment)
    form = UpdateEquipmentForm(instance=equipment)

    if request.method == 'POST':
        form = UpdateEquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('/formulation/equipmentlist/')

    context = {'form': form, 'equipment':equipment}
    return render(request, 'FormulationAndLabManagement/equipments/update_equipment.html', context)

def FL_deleteequipment(request, pk_equipment):
    equipment = equipments.objects.get(id=pk_equipment)

    if request.method == 'POST':
        equipment.delete()
        return redirect('/formulation/equipmentlist/')

    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/delete_equipment.html', context)

def FL_filtertesttubes(request):
    equipment = equipments.objects.filter(category='Test Tube')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filterflasks(request):
    equipment = equipments.objects.filter(category='Flask')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filterbeakers(request):
    equipment = equipments.objects.filter(category='Beaker')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filterpipettes(request):
    equipment = equipments.objects.filter(category='Pipette')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filterburettes(request):
    equipment = equipments.objects.filter(category='Burette')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filtercylinders(request):
    equipment = equipments.objects.filter(category='Measuring Cylinder')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filterstands(request):
    equipment = equipments.objects.filter(category='Laboratory Stand')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)

def FL_filterfunnels(request):
    equipment = equipments.objects.filter(category='Funnel')
    context = {'equipment': equipment}
    return render(request, 'FormulationAndLabManagement/equipments/filtered_equipments.html', context)


def FL_chemicaltlist(request):
    chemicals = test_chemicals.objects.all()
    available_count = chemicals.filter(status='Available').count()
    unavailable_count = chemicals.filter(status='Not Available').count()

    chemicalFilter = ChemicalFilter(request.GET, queryset=chemicals)
    chemicals = chemicalFilter.qs

    chemicallist = ['Available', 'Not Available']
    chemicalcount = [available_count, unavailable_count]

    context = {'chemicals': chemicals, 'chemicalFilter': chemicalFilter, 'chemicallist':chemicallist, 'chemicalcount':chemicalcount}
    return render(request, 'FormulationAndLabManagement/chemicals/chemical_list.html', context)

def FL_addechemical(request):
    form = AddChemicalForm()
    if request.method == 'POST':
        form = AddChemicalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/formulation/chemicallist/')

    context = {'form': form}
    return render(request, 'FormulationAndLabManagement/chemicals/add_chemical.html', context)

def FL_updatechemical(request, pk_chemical):
    chemical = test_chemicals.objects.get(id=pk_chemical)
    form = UpdateChemicalForm(instance=chemical)

    if request.method == 'POST':
        form = UpdateChemicalForm(request.POST, instance=chemical)
        if form.is_valid():
            form.save()
            return redirect('/formulation/chemicallist/')

    context = {'form': form, 'chemical': chemical}
    return render(request, 'FormulationAndLabManagement/chemicals/update_chemical.html', context)

def FL_deletechemical(request, pk_chemical):
    chemical = test_chemicals.objects.get(id=pk_chemical)

    if request.method == 'POST':
        chemical.delete()
        return redirect('/formulation/chemicallist/')

    context = {'chemical': chemical}
    return render(request, 'FormulationAndLabManagement/chemicals/delete_chemical.html', context)


def FL_test(request):
    successcount = schedule_test.objects.filter(status='Success').count()
    unsuccessscount = schedule_test.objects.filter(status='Unsuccess').count()
    pendingcount = schedule_test.objects.filter(status='Pending').count()

    statuslist = ['Success', 'Pending', 'Unsuccess']
    statuscountlist = [successcount, pendingcount, unsuccessscount,]

    context = {
        'statuslist': statuslist,
        'statuscountlist': statuscountlist,
    }
    return render(request, 'FormulationAndLabManagement/tests/tests.html', context)


def FL_scheduledtestlist(request):
    schedule_tests = schedule_test.objects.all()

    testFilter = TestFilter(request.GET, queryset=schedule_tests)
    schedule_tests = testFilter.qs

    context = {'schedule_tests': schedule_tests, 'testFilter': testFilter}
    return render(request, 'FormulationAndLabManagement/tests/sheduled_testlist.html', context)


def FL_testdetails(request, pk_test):
    scheduled_test = schedule_test.objects.get(id=pk_test)
    chemicals = scheduled_test.schedule_test_chemicals_set.all()

    context = {'scheduled_test': scheduled_test, 'chemicals': chemicals}
    return render(request, 'FormulationAndLabManagement/tests/test_details.html', context)


def FL_addtestchemicals(request, pk_test):
    ScheduledTestFormSet = inlineformset_factory(schedule_test, schedule_test_chemicals, fields=('chemical', 'quantity'), can_delete=False, extra=6)
    schedule_tests = schedule_test.objects.get(id=pk_test)
    formset = ScheduledTestFormSet(queryset=schedule_test_chemicals.objects.none(), instance=schedule_tests)
    if request.method == 'POST':
        formset = ScheduledTestFormSet(request.POST, instance=schedule_tests)
        if formset.is_valid():
            formset.save()
            return redirect('/formulation/scheduledtestslist/')

    context = {'formset': formset, 'schedule_tests': schedule_tests}
    return render(request, 'FormulationAndLabManagement/tests/chemical_formset.html', context)

def FL_edittestchemicals(request, pk_test):
    ScheduledTestFormSet = inlineformset_factory(schedule_test, schedule_test_chemicals, fields=('chemical', 'quantity'), extra=0)
    schedule_tests = schedule_test.objects.get(id=pk_test)
    formset = ScheduledTestFormSet(instance=schedule_tests)
    if request.method == 'POST':
        formset = ScheduledTestFormSet(request.POST, instance=schedule_tests)
        if formset.is_valid():
            formset.save()
            return redirect('/formulation/scheduledtestslist/')

    context = {'formset': formset, 'schedule_tests': schedule_tests}
    return render(request, 'FormulationAndLabManagement/tests/chemical_formset.html', context)

def FL_scheduletest(request):
    form = ScheduleTestForm()
    if request.method == 'POST':
        form = ScheduleTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/formulation/scheduledtestslist/')

    context = {'form': form}
    return render(request, 'FormulationAndLabManagement/tests/schedule_test.html', context)


def FL_updatetest(request, pk_test):
    schedule_tests = schedule_test.objects.get(id=pk_test)
    form = ScheduleTestForm(instance=schedule_tests)

    if request.method == 'POST':
        form = ScheduleTestForm(request.POST, request.FILES, instance=schedule_tests)
        if form.is_valid():
            form.save()
            return redirect('/formulation/scheduledtestslist/')

    context = {'form': form}
    return render(request, 'FormulationAndLabManagement/tests/schedule_test.html', context)

def FL_deletetest(request, pk_test):
    schedule_tests = schedule_test.objects.get(id=pk_test)

    if request.method == 'POST':
        schedule_tests.delete()
        return redirect('/formulation/scheduledtestslist/')

    context = {'schedule_tests': schedule_tests}
    return render(request, 'FormulationAndLabManagement/tests/delete_test.html', context)


def FL_productreport(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Product Name',
        'Category',
        'Description',
        'Preparation Method',
        'Duration' ,
        'Product Image'
    ])

    for product in products.objects.all().values_list(
            'product_name',
            'product_category',
            'description',
            'preparation_method',
            'duration',
            'product_image'
    ):
        writer.writerow(product)

    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    return response


def FL_equipmentreport(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Equipment ID',
        'Category',
        'Condition'
    ])

    for equipment in equipments.objects.all().values_list(
            'equipment_id',
            'category',
            'condition'
    ):
        writer.writerow(equipment)

    response['Content-Disposition'] = 'attachment; filename="equipments.csv"'

    return response


def FL_scheduledtesttreport(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Product',
        'Test Name',
        'Method',
        'Status',
    ])

    for test in schedule_test.objects.all().values_list(
            'product',
            'test_name',
            'method',
            'status'
    ):
        writer.writerow(test)

    response['Content-Disposition'] = 'attachment; filename="scheduled_tests.csv"'

    return response


def FL_chemicalsreport(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Chemical Name',
        'Available Quantity',
        'Status'
    ])

    for chemical in test_chemicals.objects.all().values_list(
            'chemical_name',
            'available_quantity',
            'status'
    ):
        writer.writerow(chemical)

    response['Content-Disposition'] = 'attachment; filename="chemicals.csv"'

    return response



def FL_producthistory(request):
    product = products_history.objects.all()

    productFilter = ProductsFilter(request.GET, queryset=product)
    product = productFilter.qs

    context = {'product': product, 'productFilter': productFilter}
    return render(request, 'FormulationAndLabManagement/products/product_history.html', context)


def FL_producthistoryprofile(request, pk_product):
    product = products_history.objects.get(id=pk_product)
    context = {'product': product}
    return render(request, 'FormulationAndLabManagement/products/history_profile.html', context)


def FL_producthistoryreport(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Product Name',
        'Category',
        'Description',
        'Preparation Method',
        'Duration' ,
        'Product Image',
        'Action',
        'Date',
    ])

    for product in products_history.objects.all().values_list(
            'product_name',
            'product_category',
            'description',
            'preparation_method',
            'duration',
            'product_image',
            'action',
            'date',
    ):
        writer.writerow(product)

    response['Content-Disposition'] = 'attachment; filename="product_history.csv"'

    return response













