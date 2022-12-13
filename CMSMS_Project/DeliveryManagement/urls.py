from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="DM_dashboard"),
    path('vehicleManagement/', views.vehicleManagement, name="DM_vehicleManagement"),
    path('vehicles/', views.vehicles, name="DM_vehicles"),
    path('drivers/', views.drivers, name="DM_drivers"),
    path('retail_orders/', views.retail_orders, name="DM_rOrders"),
    path('wholesale_orders/', views.wholesale_orders, name="DM_wOrders"),
    path('update_driver/<str:pk>/', views.updateDriver, name="DM_update_driver"),
    path('delete_driver/<str:pk>/', views.deleteDriver, name="DM_delete_driver"),
    path('create_driver/', views.createDriver, name="DM_create_driver"),

    path('update_vehicle/<str:pk>/', views.updateVehicle, name="DM_update_vehicle"),
    path('delete_vehicle/<str:pk>/', views.deleteVehicle, name="DM_delete_vehicle"),
    path('add_vehicle/', views.addVehicle, name="DM_add_vehicle"),
    path('add_order_items/<str:pk>/', views.addOrderItems, name="DM_add_order_items"),
    path('driver_csv/', views.driver_csv, name="driver_csv"),
    path('vehicle_csv/', views.vehicle_csv, name="vehicle_csv"),

]
