from django.urls import path
from . import views


urlpatterns = [
    # Dashboard URLs
    path('dashboard/', views.wm_dashboard, name="wm-dashboard"),
    path('esdashboard/', views.es_dashboard, name="es-dashboard"),

    # product URLs
    path('products/', views.wm_products_view, name="wm-products"),
    path('batch/', views.wm_batch_view, name="wm-batch-received"),
    path('batch/status/change/<str:pk>/', views.wm_batch_status_change, name="wm-batch-status-change"),
    path('product/details/<str:pk>/', views.wm_product_details, name="wm-products-view"),
    path('product/update/<str:pk>/', views.wm_product_update, name="wm-products-update"),
    path('product/delete/<str:pk>/', views.wm_product_delete, name="wm-products-delete"),
    path('product/reorder/<str:pk>/', views.wm_product_reorder, name="wm-products-reorder"),

    # Request URLs
    path('reorder/', views.wm_reorder, name="wm-reorder"),
    path('requests/supplier/', views.wm_request_supplier, name="wm-requests-supplier"),
    path('requests/batch/', views.wm_request_batch, name="wm-requests-batch"),
    path('requests/from/batch/', views.wm_request_from_batch, name="wm-requests-from-batch"),
    path('requests/batch/update/<str:pk>/', views.wm_request_batch_status_update, name="wm-batch-req-status-update"),
    path('requests/update/<str:pk>/', views.wm_request_update, name="wm-request-update"),
    path('requests/delete/<str:pk>/', views.wm_request_delete, name="wm-request-delete"),

    # Inventory URLs
    path('inventory/', views.wm_inventory, name="wm-inventory"),

    path('inventory/Rawmaterials/', views.wm_rawmaterials, name="wm-raw-materials"),
    path('inventory/rawmaterial/details/<str:pk>/', views.wm_rawmaterial_details, name="wm-raw-material-view"),
    path('inventory/rawmaterial/update/<str:pk>/', views.wm_rawmaterial_update, name="wm-raw-material-update"),
    path('inventory/rawmaterial/delete/<str:pk>/', views.wm_rawmaterial_delete, name="wm-raw-material-delete"),
    path('inventory/rawmaterial/reorder/<str:pk>/', views.wm_rawmaterial_reorder, name="wm-raw-material-reorder"),

    path('inventory/equipments/', views.wm_equipments, name="wm-equipments"),
    path('inventory/equipment/details/<str:pk>/', views.wm_equipment_details, name="wm-equipment-view"),
    path('inventory/equipment/update/<str:pk>/', views.wm_equipment_update, name="wm-equipment-update"),
    path('inventory/equipment/delete/<str:pk>/', views.wm_equipment_delete, name="wm-equipment-delete"),

    path('inventory/packaging/', views.wm_packaging, name="wm-packaging"),
    path('inventory/packaging/details/<str:pk>/', views.wm_packaging_details, name="wm-packaging-view"),
    path('inventory/packaging/update/<str:pk>/', views.wm_packaging_update, name="wm-packaging-update"),
    path('inventory/packaging/delete/<str:pk>/', views.wm_packaging_delete, name="wm-packaging-delete"),
    path('inventory/packaging/reorder/<str:pk>/', views.wm_packaging_reorder, name="wm-packaging-reorder"),

    # Orders URLs
    path('orders/', views.wm_orders, name="wm-orders"),
    path('order/start/<str:pk>/', views.wm_order_start, name="wm-order-start"),
    path('order/complete/<str:pk>/', views.wm_order_complete, name="wm-order-complete"),
    path('order/finish/<str:pk>/', views.wm_order_finish, name="wm-order-finish"),
    path('order/remove/<str:pk>/', views.wm_order_remove, name="wm-order-remove"),
    path('order/reset/<str:pk>/', views.wm_order_reset, name="wm-order-reset"),

    # Employee URLs
    path('employees/', views.wm_employees, name="wm-employees"),
    path('employee/accept/<str:pk>/', views.wm_employee_accept, name="wm-employee-accept"),
    path('employee/new/view/<str:pk>/', views.wm_employee_new_view, name="wm-new-employee-view"),
    path('employee/view/<str:pk>/', views.wm_employee_view, name="wm-employee-view"),
    path('employee/update/<str:pk>/', views.wm_employee_update, name="wm-employee-update"),
    path('employee/remove/<str:pk>/', views.wm_employee_remove, name="wm-employee-remove"),
    path('employee/assign/<str:pk>/', views.wm_employee_assign, name="wm-employee-assign"),
    path('employee/free/<str:pk>/', views.wm_employee_free, name="wm-employee-free"),

    # History URLs
    path('history/', views.wm_history, name="wm-history"),
    path('history/clear/', views.wm_history_clear, name="wm-history-clean"),

]
