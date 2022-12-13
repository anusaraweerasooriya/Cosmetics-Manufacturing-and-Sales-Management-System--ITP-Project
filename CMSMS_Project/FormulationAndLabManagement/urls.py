from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.FL_dashboard, name="FL_dashboard"),


    path('productsdashboard/', views.FL_productsdashboard, name="FL_productsdashboard"),
    path('addproduct/', views.FL_addproducts, name="FL_addproducts"),
    path('updateproduct/<str:pk_product>/', views.FL_updateproduct, name="FL_updateproduct"),
    path('deleteproduct/<str:pk_product>/', views.FL_deleteproduct, name="FL_deleteproduct"),

    path('product_profile/<str:pk_product>/', views.FL_productprofile, name="FL_productprofile"),
    path('products/', views.FL_products, name="FL_products"),
    path('filteredproducts/', views.FL_filteredproducts, name="FL_filteredproducts"),
    path('skincosmetics/', views.FL_filterskincosmetics, name="FL_filterskincosmetics"),
    path('haircosmetics/', views.FL_filterhaircosmetics, name="FL_filterhaircosmetics"),
    path('nailcosmetics/', views.FL_filternailcosmetics, name="FL_filternailcosmetics"),
    path('facemakeup/', views.FL_filterfacemakeup, name="FL_filterfacemakeup"),


    path('addformulation/<str:pk_product>/', views.FL_formulation, name="FL_addformulation"),
    path('editformulation/<str:pk_product>/', views.FL_editformulation, name="FL_editformulation"),


    path('equipments/', views.FL_equipments, name="FL_equipments"),
    path('addequipments/', views.FL_addequipments, name="FL_addequipments"),
    path('updateequipment/<str:pk_equipment>/', views.FL_updateequipment, name="FL_updateequipment"),
    path('deleteequipment/<str:pk_equipment>/', views.FL_deleteequipment, name="FL_deleteequipment"),

    path('equipmentlist/', views.FL_equipmentlist, name="FL_equipmentlist"),
    path('filteredequipments/', views.FL_filteredequipments, name="FL_filteredequipments"),
    path('testtubelist/', views.FL_filtertesttubes, name="FL_filtertesttubes"),
    path('flasklist/', views.FL_filterflasks, name="FL_filterflasks"),
    path('beakerlist/', views.FL_filterbeakers, name="FL_filterbeakers"),
    path('pipettelist/', views.FL_filterpipettes, name="FL_filterpipettes"),
    path('burettelist/', views.FL_filterburettes, name="FL_filterburettes"),
    path('cylinderlist/', views.FL_filtercylinders, name="FL_filtercylinders"),
    path('standlist/', views.FL_filterstands, name="FL_filterstands"),
    path('funnellist/', views.FL_filterfunnels, name="FL_filterfunnels"),


    path('chemicallist/', views.FL_chemicaltlist, name="FL_chemicallist"),
    path('addechemical/', views.FL_addechemical, name="FL_addechemical"),
    path('updateechemical/<str:pk_chemical>/', views.FL_updatechemical, name="FL_updatechemical"),
    path('deleteechemical/<str:pk_chemical>/', views.FL_deletechemical, name="FL_deletechemical"),


    path('test/', views.FL_test, name="FL_test"),
    path('scheduledtestslist/', views.FL_scheduledtestlist, name="FL_scheduledtestlist"),
    path('testdetails/<str:pk_test>/', views.FL_testdetails, name="FL_testdetails"),
    path('scheduletest/', views.FL_scheduletest, name="FL_scheduletest"),
    path('updatetest/<str:pk_test>/', views.FL_updatetest, name="FL_updatetest"),
    path('deletetest/<str:pk_test>/', views.FL_deletetest, name="FL_deletetest"),


    path('addtestchemicals/<str:pk_test>/', views.FL_addtestchemicals, name="FL_addtestchemicals"),
    path('edittestchemicals/<str:pk_test>/', views.FL_edittestchemicals, name="FL_edittestchemicals"),


    path('productreport/', views.FL_productreport, name="FL_productreport"),
    path('equipmentreport/', views.FL_equipmentreport, name="FL_equipmentreport"),
    path('scheduledtesttreport/', views.FL_scheduledtesttreport, name="FL_scheduledtesttreport"),
    path('chemicalreport/', views.FL_chemicalsreport, name="FL_chemicalsreport"),
    path('producthistoryreport/', views.FL_producthistoryreport, name="FL_producthistoryreport"),

    path('producthistory/', views.FL_producthistory, name="FL_producthistory"),
    path('producthistoryprofile/<str:pk_product>/', views.FL_producthistoryprofile, name="FL_producthistoryprofile"),
    path('deletehistory', views.FL_deleteproducthistory, name="FL_deleteproducthistory"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)