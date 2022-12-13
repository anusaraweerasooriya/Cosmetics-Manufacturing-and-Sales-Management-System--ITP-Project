import csv
from itertools import chain
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from .models import *
from .models import ProductionCost, Production, DirectMaterialCost, DirectLaborCost, FactoryOverheads
from django.http import HttpResponse
from datetime import datetime
from .forms import *
from django.core.paginator import Paginator
from .decorators import cost_manager_only
from django.contrib import messages
import json
from django.http import JsonResponse
from .filters import *


# Create your views here.


def index(request):
    return render(request, 'CostAnalysisManagement/CA_partials/CA_base.html')


def messages(request):
    return render(request, 'CostAnalysisManagement/CA_partials/messages.html')


@cost_manager_only
def CA_dashboard(request):
    products = Production.objects.all()
    product_count = products.count()
    product_category = products.count()
    materials_count = products.count()

    context = {
        "production": products,
        "product_count": product_count,
        "product_category": product_category,
        "materials_count": materials_count,
    }
    return render(request, 'CostAnalysisManagement/CA_dashboard/index.html', context)


def index(request):
    index = Expenses.objects.all()

    expense_filter = ExpensesFilter(request.GET, queryset=index)
    index = expense_filter.qs

    context = {
        'index': index,
        'expense_filter': expense_filter,
    }
    return render(request, 'CostAnalysisManagement/expenses/index.html', context)


def add_expense(request):
    form = AddExpenses()

    if request.method == 'POST':
        form = AddExpenses(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form
    }
    return render(request, 'CostAnalysisManagement/expenses/add_expense.html', context)


def update_expenses(request, pk):
    index = Expenses.objects.get(id=pk)
    form = AddExpenses(instance=index)

    if request.method == 'POST':
        form = AddExpenses(request.POST, instance=index)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
        'index': index
    }
    return render(request, 'CostAnalysisManagement/expenses/update_expenses.html', context)


def delete_expeses(request, pk):
    index = Expenses.objects.get(id=pk)

    if request.method == 'POST':
        index.delete()
        return redirect('index')

    context = {
        'index': index
    }
    return render(request, 'CostAnalysisManagement/expenses/delete_expenses.html', context)


def income(request):
    income = Income.objects.all()

    income_filter = IncomeFilter(request.GET, queryset=income)
    income = income_filter.qs

    context = {
        'income': income,
        'income_filter': income_filter,
    }

    return render(request, 'CostAnalysisManagement/income/income.html', context)


def add_income(request):
    form = AddIncome()

    if request.method == 'POST':
        form = AddIncome(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income')

    context = {
        'form': form
    }
    return render(request, 'CostAnalysisManagement/income/add_income.html', context)


def update_income(request, pk):
    income = Income.objects.get(id=pk)
    form = AddIncome(instance=income)

    if request.method == 'POST':
        form = AddIncome(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income')

    context = {
        'form': form,
        'income': income
    }
    return render(request, 'CostAnalysisManagement/income/edit_income.html', context)


def delete_income(request, pk):
    income = Income.objects.get(id=pk)

    if request.method == 'POST':
        income.delete()
        return redirect('income')

    context = {
        'income': income
    }
    return render(request, 'CostAnalysisManagement/income/delete_income.html', context)



def production_cost(request):
    production_cost = ProductionCost.objects.all()

    pc_filter = ProductionCostFilter(request.GET, queryset=production_cost)
    production_cost = pc_filter.qs

    context = {
        'production_cost': production_cost,
        'pc_filter': pc_filter,
    }

    return render(request, 'CostAnalysisManagement/production_cost/production_cost.html', context)


def add_proCost(request):
    form = AddProductionCostForm()

    if request.method == 'POST':
        form = AddProductionCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('production-cost')

    context = {
        'form': form
    }
    return render(request, 'CostAnalysisManagement/production_cost/add_proCost.html', context)


def update_production_cost(request, pk):
    production_cost = ProductionCost.objects.get(id=pk)
    form = AddProductionCostForm(instance=production_cost)

    if request.method == 'POST':
        form = AddProductionCostForm(request.POST, instance=production_cost)
        if form.is_valid():
            form.save()
            return redirect('production-cost')

    context = {
        'form': form,
        'production_cost': production_cost
    }
    return render(request, 'CostAnalysisManagement/production_cost/Update_proCost.html', context)


def delete_production_cost(request, pk):
    production_cost = ProductionCost.objects.get(id=pk)

    if request.method == 'POST':
        production_cost.delete()
        return redirect('production-cost')

    context = {'productin_cost': production_cost}
    return render(request, 'CostAnalysisManagement/production_cost/delete_proCost.html', context)


def directmaterial_cost(request):
    directmaterial_cost = DirectMaterialCost.objects.all()

    dm_filter = DirectMaterialCostFilter(request.GET, queryset=directmaterial_cost)
    directmaterial_cost = dm_filter.qs

    context = {
        'directmaterial_cost': directmaterial_cost,
        'dm_filter': dm_filter,
    }
    return render(request, 'CostAnalysisManagement/Direct_MaterialCost/directmaterial_cost.html', context)


def add_directmaterial_cost(request):
    form = AddDirectMaterialCostForm()

    if request.method == 'POST':
        form = AddDirectMaterialCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directmaterial-cost')

    context = {
        'form': form
    }
    return render(request, 'CostAnalysisManagement/Direct_MaterialCost/add_dmCost.html', context)


def update_directmaterial_cost(request, pk):
    directmaterial_cost = DirectMaterialCost.objects.get(id=pk)
    form = AddDirectMaterialCostForm(instance=directmaterial_cost)

    if request.method == 'POST':
        form = AddDirectMaterialCostForm(request.POST, instance=directmaterial_cost)
        if form.is_valid():
            form.save()
            return redirect('directmaterial-cost')

    context = {
        'form': form,
        'directmaterial_cost': directmaterial_cost
    }
    return render(request, 'CostAnalysisManagement/Direct_MaterialCost/update_dmCost.html', context)


def delete_directmaterial_cost(request, pk):
    directmaterial_cost = DirectMaterialCost.objects.get(id=pk)

    if request.method == 'POST':
        directmaterial_cost.delete()
        return redirect('directmaterial-cost')

    context = {
        'directmaterial_cost': directmaterial_cost
    }
    return render(request, 'CostAnalysisManagement/Direct_MaterialCost/delete_dmCost.html', context)


def directlabor_cost(request):
    directlabor_cost = DirectLaborCost.objects.all()

    dl_filter = DirectLaborCostFilter(request.GET, queryset=directlabor_cost)
    directlabor_cost = dl_filter.qs

    context = {
        'directlabor_cost': directlabor_cost,
        'dl_filter': dl_filter,

    }
    return render(request, 'CostAnalysisManagement/Direct_LaborCost/directlabor_cost.html', context)


def add_directlabor_cost(request):
    form = AddDirectLaborCostForm()

    if request.method == 'POST':
        form = AddDirectLaborCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directlabor-cost')

    context = {
        'form': form
    }
    return render(request, 'CostAnalysisManagement/Direct_LaborCost/add_dlCost.html', context)


def update_directlabor_cost(request, pk):
    directlabor_cost = DirectLaborCost.objects.get(id=pk)
    form = AddDirectLaborCostForm(instance=directlabor_cost)

    if request.method == 'POST':
        form = AddDirectLaborCostForm(request.POST, instance=directlabor_cost)
        if form.is_valid():
            form.save()
            return redirect('directlabor-cost')

    context = {
        'form': form,
        'directlabor_cost': directlabor_cost
    }
    return render(request, 'CostAnalysisManagement/Direct_LaborCost/update_dlCost.html', context)


def delete_directlabor_cost(request, pk):
    directlabor_cost = DirectLaborCost.objects.get(id=pk)

    if request.method == 'POST':
        directlabor_cost.delete()
        return redirect('directlabor-cost')

    context = {
        'directlabor_cost': directlabor_cost
    }
    return render(request, 'CostAnalysisManagement/Direct_LaborCost/delete_dlCost.html', context)


def factory_overheads_cost(request):
    factory_overheads_cost = FactoryOverheads.objects.all()

    fo_filter = FactoryOverheadsFilter(request.GET, queryset=factory_overheads_cost)
    factory_overheads_cost = fo_filter.qs

    context = {
        'factory_overheads_cost': factory_overheads_cost,
        'fo_filter': fo_filter
    }
    return render(request, 'CostAnalysisManagement/Factory_Overhead_cost/factory_overheads_cost.html', context)


def add_factory_overheads_cost(request):
    form = AddFactoryOverheadCostForm

    if request.method == 'POST':
        form = AddFactoryOverheadCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('factoryoverheads-cost')

    context = {
        'form': form
    }
    return render(request, 'CostAnalysisManagement/Factory_Overhead_cost/add_foCost.html', context)


def update_factory_overheads_cost(request, pk):
    factory_overheads_cost = FactoryOverheads.objects.get(id=pk)
    form = AddFactoryOverheadCostForm(instance=factory_overheads_cost)

    if request.method == 'POST':
        form = AddFactoryOverheadCostForm(request.POST, instance=factory_overheads_cost)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('factoryoverheads-cost')

    context = {
        'factory_overheads_cost': factory_overheads_cost
    }
    return render(request, 'CostAnalysisManagement/Factory_Overhead_cost/update_foCost.html', context)


def delete_factory_overheads_cost(request, pk):
    factory_overheads_cost = FactoryOverheads.objects.get(id=pk)

    if request.method == 'POST':
        factory_overheads_cost.delete()
        return redirect('factoryoverheads-cost')

    context = {
        'factory_overheads_cost': factory_overheads_cost
    }
    return render(request, 'CostAnalysisManagement/Factory_Overhead_cost/delete_foCost.html', context)


def retail_price(request):
    retail_price = RetailPrice.objects.all()

    rp_filter = FactoryOverheadsFilter(request.GET, queryset=retail_price)
    retail_price = rp_filter.qs

    context = {
        'retail_price': retail_price,
        'rp_filter': rp_filter
    }
    return render(request, 'CostAnalysisManagement/RetailPrice/retailPrice.html')


def add_retail_price(request):
    form = RetailPriceForm

    if request.method == 'POST':
        form = RetailPriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('retail-price')

    context = {
        'form': form
    }

    return render(request, 'CostAnalysisManagement/RetailPrice/add_retailPrice.html')


def update_retail_price(request, pk):
    retail_price = RetailPrice.objects.get(id=pk)
    form = RetailPriceForm(instance=retail_price)

    if request.method == 'POST':
        form = RetailPriceForm(request.POST, instance=retail_price)
        if form.is_valid():
            form.save()
            return redirect('retail-price')

    context = {
        'retail_price': retail_price
    }
    return render(request, 'CostAnalysisManagement/RetailPrice/update_retailPrice.html', context)


def delete_retail_price(request, pk):
    delete_retail_price = RetailPrice.objects.get(id=pk)

    if request.method == 'POST':
        delete_retail_price.delete()
        return redirect('retail-price')

    context = {
        'delete_retail_price': delete_retail_price
    }
    return render(request, 'CostAnalysisManagement/RetailPrice/delete_retailPrice.html', context)


def profile(request):
    return render(request, 'CostAnalysisManagement/CA_account/profile.html')


# ------------------------report generation----------------------------------------
def expensesCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expenses_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date', 'Type'])

    expenses = Expenses.objects.all()
    for ex in expenses:
        writer.writerow([ex.id, ex.amount, ex.date, ex.type])

    return response


def productionCostCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=production_cost_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date', 'Category', 'Description'])

    production_cost = ProductionCost.objects.all()
    for pc in production_cost:
        writer.writerow([pc.id, pc.amount, pc.date, pc.category, pc.description])

    return response


def directMaterialCostCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=directMaterial_cost_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date', 'Category', 'Description'])

    directmaterial_cost = DirectMaterialCost.objects.all()
    for dm in directmaterial_cost:
        writer.writerow([dm.id, dm.Total_DMAmount, dm.date, dm.category, dm.description])

    return response


def directLaborCostCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=directLabor_cost_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date', 'Category', 'Description'])

    directlabor_cost = DirectLaborCost.objects.all()
    for dl in directlabor_cost:
        writer.writerow([dl.id, dl.Total_DLAmount, dl.date, dl.category, dl.description])

    return response


def factoryOverheadsCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=factory_overheads_cost_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date', 'Category', 'Description'])

    factory_overheads_cost = FactoryOverheads.objects.all()
    for fo in factory_overheads_cost:
        writer.writerow([fo.id, fo.Total_FOAmount, fo.date, fo.category, fo.description])

    return response


def incomeCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=income_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date'])

    income = Expenses.objects.all()
    for ix in income:
        writer.writerow([ix.id, ix.amount, ix.date])

    return response


def retailCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=retail_price_report.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Amount', 'Date'])

    retail_price = Expenses.objects.all()
    for rx in retail_price:
        writer.writerow([rx.id, rx.amount, rx.date])

    return response



