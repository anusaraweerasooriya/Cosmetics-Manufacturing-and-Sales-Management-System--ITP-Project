from django.urls import path
from . import views

urlpatterns = [
    # Dashboard urls
    path('', views.dashboard, name="bp_dashboard"),

    # Materials urls
    path('bp_rawmaterials/', views.rawmaterials, name="bp_rawmaterials"),
    path('bp_create_rawmaterial/', views.createRawmaterial, name="bp_create_rawmaterial"),
    path('bp_update_rawmaterial/<str:pk>/', views.updateRawmaterial, name="bp_update_rawmaterial"),
    path('bp_delete_rawmaterial/<str:pk>/', views.deleteRawmaterial, name="bp_delete_rawmaterial"),
    path('bp_deficiency_request/<str:pk>/', views.deficiencyRequest, name="bp_deficiency_request"),
    path('bp_materials_csv/', views.materialsCSV, name="bp_materials_csv"),

    # Requests urls
    path('bp_requests/', views.requests, name="bp_requests"),
    path('bp_create_request/', views.createRequest, name="bp_create_request"),
    path('bp_update_request/<str:pk>/', views.updateRequest, name="bp_update_request"),
    path('bp_delete_request/<str:pk>/', views.deleteRequest, name="bp_delete_request"),
    path('bp_request_received/<str:pk>/', views.requestReceived, name="bp_request_received"),
    path('bp_delete_completed_request/<str:pk>/', views.requestCompletedDelete, name="bp_delete_completed_request"),
    path('bp_requests_csv/', views.requestsCSV, name="bp_requests_csv"),

    # Products/Scheduling urls
    path('bp_products/', views.getProducts, name="bp_products"),
    path('bp_view_product/<str:pk>/', views.viewProduct, name="bp_view_product"),
    path('bp_schedule_production/<str:pk>/', views.scheduleProduction, name="bp_schedule_production"),
    path('bp_confirm_schedule/<str:pk>/', views.confirmSchedule, name="bp_confirm_schedule"),
    path('bp_confirm_onhold/<str:pk>/', views.confirmOnHold, name="bp_confirm_onhold"),
    path('bp_delete_production/<str:pk>/', views.deleteProduction, name="bp_delete_production"),
    path('bp_proceed_schedule/<str:pk>/', views.proceedSchedule, name="bp_proceed_schedule"),
    path('bp_deficiency_request_on_schedule/<str:pk>/<str:pk2>/', views.deficiencyRequestOnSchedule, name="bp_deficiency_request_on_schedule"),
    path('bp_cancel_schedule/<str:pk>/', views.cancelSchedule, name="bp_cancel_schedule"),

    # Productions urls
    path('bp_batch_productions/', views.batchProductions, name="bp_bproductions"),
    path('bp_update_production/<str:pk>/', views.updateProduction, name="bp_update_production"),
    path('bp_delete_production/<str:pk>/', views.deleteProduction, name="bp_delete_production"),
    path('bp_view_scheduled/<str:pk>/', views.viewScheduled, name="bp_view_scheduled"),
    path('bp_proceed_production/<str:pk>/', views.proceedProduction, name="bp_proceed_production"),
    path('bp_view_onhold/<str:pk>/', views.viewOnHold, name="bp_view_onhold"),
    path('bp_deficiency_request_on_hold/<str:pk>/<str:pk2>/<str:pk3>/', views.deficiencyRequestOnHold, name="bp_deficiency_request_on_hold"),
    path('bp_confirm_schedule_after_onhold/<str:pk>/', views.confirmScheduleOnHold, name="bp_confirm_schedule_after_onhold"),
    path('bp_complete_production/<str:pk>/', views.completeProduction, name="bp_complete_production"),
    path('bp_productions_csv/', views.productionsCSV, name="bp_productions_csv"),

    # Batches urls
    path('bp_batches/', views.batches, name="bp_batches"),
    path('bp_batch_dispatch/<str:pk>/', views.batchDispatch, name="bp_batch_dispatch"),
    path('bp_batch_requests/', views.batch_requests, name="bp_batch_requests"),
    path('bp_view_batch_request/<str:pk>/', views.view_batch_request, name="bp_view_batch_request"),
    path('bp_dispatch_batch_request/<str:pk>/<str:pk2>/', views.dispatchBatchRequest, name="bp_dispatch_batch_request"),
    path('bp_schedule_batch_request/<str:pk>/', views.schedule_batch_request, name="bp_schedule_batch_request"),
    path('bp_batches_csv/', views.batchesCSV, name="bp_batches_csv"),

    # Machinery
    path('bp_machinery/', views.machinery, name="bp_machinery"),
    path('bp_add_machinery/', views.createMachinery, name="bp_add_machinery"),
    path('bp_view_machinery/<str:pk>/', views.view_machinery, name="bp_view_machinery"),
    path('bp_update_machinery/<str:pk>/', views.updateMachinery, name="bp_update_machinery"),
    path('bp_delete_machinery/<str:pk>/', views.deleteMachinery, name="bp_delete_machinery"),
    path('bp_machinery_csv/', views.machineryCSV, name="bp_machinery_csv"),

    # History urls
    path('bp_material_history/', views.rawmaterial_history, name="bp_material_history"),
    path('bp_clear_material_history/', views.clear_rawmaterial_history, name="bp_clear_material_history"),



]