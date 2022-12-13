import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from CustomerAndSalesManagement.models import Order as RetailOrders
from CustomerAndSalesManagement.models import OrderItem as RetailOrderItems
from .filters import DriverFilter, VehicleFilter


# Create your views here ...
def dashboard(request):
    need_repair = Vehicle.objects.filter(condition='Need to be repaired').count()
    good_condition = Vehicle.objects.filter(condition='Good condition').count()

    context = {
        'need_repair': need_repair,
        'good_condition': good_condition
    }
    return render(request, 'DeliveryManagement/dashboard.html', context)


def vehicleManagement(request):
    return render(request, 'DeliveryManagement/vehicleManagement.html')


def vehicles(request):
    vehicles = Vehicle.objects.all()

    myFilter = VehicleFilter(request.GET, queryset=vehicles)
    vehicles = myFilter.qs

    context = {
        'vehicles': vehicles, 'myFilter': myFilter
    }
    return render(request, 'DeliveryManagement/vehicles.html', context)


def drivers(request):
    drivers = Driver.objects.all()

    myFilter = DriverFilter(request.GET, queryset=drivers)
    drivers = myFilter.qs

    context = {
        'drivers': drivers, 'myFilter': myFilter
    }
    return render(request, 'DeliveryManagement/drivers.html', context)


def retail_orders(request):
    orders = RetailOrders.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'DeliveryManagement/retailOrders.html', context)


def wholesale_orders(request):
    return render(request, 'DeliveryManagement/wholesaleOrders.html')


def updateDriver(request, pk):
    driver = Driver.objects.get(id=pk)
    form = DriverForm(instance=driver)

    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('/delivery/drivers')

    context = {
        'form': form,
    }
    return render(request, 'DeliveryManagement/driver_form.html', context)


def deleteDriver(request, pk):
    driver = Driver.objects.get(id=pk)

    if request.method == 'POST':
        driver.delete()
        return redirect('DM_drivers')

    context = {
        'driver': driver,
    }
    return render(request, 'DeliveryManagement/delete_driver.html', context)


def createDriver(request):
    form = DriverForm()

    if request.method == 'POST':
        # print('Printing Post:', request.POST)
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/delivery/drivers')

    context = {
        'form': form
    }
    return render(request, 'DeliveryManagement/driver_form.html', context)


def updateVehicle(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    form = VehicleForm(instance=vehicle)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('/delivery/vehicles')

    context = {
        'form': form,
    }
    return render(request, 'DeliveryManagement/vehicle_form.html', context)


def deleteVehicle(request, pk):
    vehicle = Vehicle.objects.get(id=pk)

    if request.method == 'POST':
        vehicle.delete()
        return redirect('DM_vehicles')

    context = {
        'vehicle': vehicle,
    }
    return render(request, 'DeliveryManagement/delete_vehicle.html', context)


def addVehicle(request):
    form = VehicleForm()

    if request.method == 'POST':
        # print('Printing Post:', request.POST)
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/delivery/vehicles')

    context = {
        'form': form
    }
    return render(request, 'DeliveryManagement/vehicle_form.html', context)


def addOrderItems(request, pk):
    form = OrderItemRequestForm()

    requested_items = Order.objects.all().values('id')
    order_items = RetailOrderItems.objects.all().exclude(id__in=requested_items)

    if request.method == 'POST':
        form = OrderItemRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/delivery/addOrderItems')

    context = {
        'form': form,
        'order_items': order_items,
    }

    return render(request, 'DeliveryManagement/add_order_items.html', context)


# Drivers CSV
def driver_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=drivers.csv'

    # Create CSV Writer
    writer = csv.writer(response)

    drivers = Driver.objects.all()

    # Add column headings to the csv file
    writer.writerow([
        'Full Name',
        'Contact Nuber',
        'Email',
        'Gender',
        'License Number',
        'NIC',
        'License Valid',
    ])

    # Loop through and output
    for driver in drivers:
        writer.writerow([driver.fullname,
                         driver.contact_number,
                         driver.email,
                         driver.gender,
                         driver.LicenseNumber,
                         driver.nic,
                         driver.LicenseValid,
                         ])

    return response


# Vehicles CSV
def vehicle_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=vehicles.csv'

    # Create CSV Writer
    writer = csv.writer(response)

    vehicles = Vehicle.objects.all()

    # Add column headings to the csv file
    writer.writerow([
        'Driver',
        'Model of the Vehicle',
        'Brand',
        'Trim',
        'License Plate',
        'Exterior Color',
        'Year',
        'Engine Capacity',
        'Mileage',
        'Fuel Type',
        'Quantity',
        'condition',
        'Transmission',
    ])

    # Loop through and output
    for vehicle in vehicles:
        writer.writerow([vehicle.driver,
                         vehicle.modelVehicle,
                         vehicle.brand,
                         vehicle.trim,
                         vehicle.LicensePlate,
                         vehicle.exteriorColor,
                         vehicle.year,
                         vehicle.engineCapacity,
                         vehicle.mileage,
                         vehicle.fuelType,
                         vehicle.quantity,
                         vehicle.condition,
                         vehicle.transmission,
                         ])

    return response
