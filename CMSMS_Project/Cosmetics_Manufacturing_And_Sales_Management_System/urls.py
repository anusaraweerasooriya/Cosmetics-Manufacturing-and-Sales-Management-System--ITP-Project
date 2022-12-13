from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('warehouse/', include('WarehouseManagement.urls')),
    path('customer_sales/', include('CustomerAndSalesManagement.urls')),
    path('supplierManagement/', include('SupplierManagement.urls')),
    path('batch/', include('BatchProductionManagement.urls')),
    path('', include('Users.urls')),
    path('formulation/', include('FormulationAndLabManagement.urls')),
    path('delivery/', include('DeliveryManagement.urls')),
    path('Cost/', include('CostAnalysisManagement.urls')),
    path('employee/', include('EmployeeManagement.urls')),
    path(r'"download/(?p<path>.")$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
