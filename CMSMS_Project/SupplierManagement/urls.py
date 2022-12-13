from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('SMdashboard/', views.SM_dashboard, name='SM_dashboard-SM_dashboard'),
    path('Supplierdashboard/', views.Supplier_dashboard, name='S_dashboard-Supplier_dashboard'),
    path('Suppliers/', views.Suppliers, name='SM_dashboard-Suppliers'),
    path('Suppliers/ViewSupplier/<str:pk>/', views.ViewSupplier, name='SM_dashboard-Supplier-View'),
    path('Supplier/RemoveSupplier/<str:pk>/', views.RemoveSupplier, name='SM_dashboard-Supplier-Remove'),

    path('WarehouseRequests/', views.Warehouserequests, name='SM_dashboard-WarehouseRequests'),
    path('WarehouseRequests/RequestOrder/<str:pk>', views.RequestOrder, name='SM_dashboard-RequestOrder'),
    path('WarehouseRequests/<str:pk>', views.whrequestview, name='SM_dashboard-whrequests-view'),

    path('NewSuppliers/', views.newsupplier, name='SM_dashboard-NewSupplier'),
    path('SupplierRegister/', views.SupplierRegistration, name='SM_User-Register'),
    path('NewSuppliers/ViewNewSuppliers/<str:pk>/', views.ViewNewSuppliers, name='SM_dashboard-NewSupplier-View'),
    path('NewSuppliers/AcceptSupplier/<str:pk>/', views.AcceptSupplier, name='SM_dashboard-NewSupplier-Accept'),
    path('NewSuppliers/RejectSupplier/<str:pk>/', views.RejectSupplier, name='SM_dashboard-NewSupplier-Reject'),
    path('NewSuppliers/<str:pk>/', views.RemoveNewSupplier, name='SM_dashboard-NewSupplier-Remove'),

    path('OrderRequests', views.orderRequests, name='SM_dashboard-OrderRequests'),
    path('OrderRequests/PendingRequests/', views.pendingrequests, name='SM_dashboard-PendingRequests'),
    path('OrderRequests/ToPay/', views.toPay, name='SM_dashboard-ToPay'),
    path('OrderRequests/ToReOrder/', views.to_reorder, name='SM_dashboard-To_reorder'),
    path('OrdersRequests/ToReOrder/ReOrder/<str:pk>/', views.Re_Order, name='SM_dashboard-RequestOrder-Reorder'),
    path('OrderRequests/Remove/<str:pk>/', views.RemoveRequest, name='SM-dashboard-RequestOrder-Remove'),
    path('OrderRequests/Cancel/<str:pk>/', views.CancelOrder, name='SM-dashboard-RequestOrder-Cancel'),
    path('OrderRequests/Invoice/<str:pk>/', views.Invoice, name='SM-dashboard-RequestOrder-Invoice'),
    path('OrderRequests/Order/<str:pk>/', views.makeOrder, name='SM-dashboard-RequestOrder-Order'),

    path('SupplierProducts/', views.products, name='S_dashboard-Products'),
    path('SupplierProducts/DeleteProduct/<str:pk>/', views.productDelete, name='S_dashboard-Products-delete'),
    path('SupplierProducts/UpdateProduct/<str:pk>/', views.productsUpdate, name='S_dashboard-Products-update'),

    path('Requests/', views.smrequests, name='S_dashboard-Requests'),
    path('Requests/Accept/<str:pk>/', views.acceptorder, name='S_dashboard-Requests-Accept'),
    path('Requests/Reject/<str:pk>/', views.rejectorder, name='S_dashboard-Requests-Reject'),
    path('Requests/View/<str:pk>/', views.reqOrderView, name='S_dashboard-Requests-View'),

    path('MyOrders/', views.ordersReceived, name='S_dashboard-MyOrders'),
    path('MyOrders/OrderView/<str:pk>/', views.orderView, name='S_dashboard-MyOrders-View'),
    path('Myorders/Neworders/', views.neworders, name='S_dashboard-MyOrders-NewOrders'),

    path('OrderHistoty/', views.sm_orderhistory, name='SM_dashbboard-OrderHistory'),
    path('OrderHistoty/MarkReceieved/<str:pk>/', views.markReceived, name='SM_dashboard-OrderHistory-received'),
    path('OrderHistory/View/<str:pk>/', views.orderInfo, name='SM_dashboard-OrderHistory-view'),
    path('OrderHistory/ReturnRequest/<str:pk>/', views.returnRequest, name='SM_dashboard-ReturnRequest'),

    path('Profile/', views.profile, name='SM_user-Profile'),
    path('Profile/UpdateProfile/', views.SprofileUpdate, name='SM_user-UpdateProfile'),
    path('Profile/ProfileUpdate/', views.SMprofileUpdate, name='SM_user-SMUpdateProfile'),
    path('Profile/ChangePassword/', auth_views.PasswordChangeView.as_view(template_name='SM_user/changePassword.html', success_url='/warehouse/dashboard/'), name='SM_user-ChangePassword'),

    path('ToRefund/', views.torefund, name='S_dashboard-ToRefund'),
    path('ToRefund/Refund/<str:pk>/', views.refund, name='S_dashboard-Refund'),
    path('ToRefund/Refund/success/', views.paymentsuccess, name='S_dashboard-Refund-Success'),

    path('RefundedItems/', views.refundeditems, name='S_dashboard-Refunded'),
    path('SMRefundedItems/', views.refundedlist, name='SM_dashboard-RefundedItems'),

]