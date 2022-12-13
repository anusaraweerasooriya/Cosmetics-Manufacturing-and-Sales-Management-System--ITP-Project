from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('customer_home/', views.customer_home, name="customer_home"),
    path('customer_products/', views.sales_product, name="customer_products"),
    path('customer_product_page/<str:pk>', views.customer_product_page, name='customer_product_page'),

    path('customer_register/', views.customer_registration, name="customer_register"),
    path('customer_login/', views.customer_login, name="customer_login"),
    path('customer_logout/', views.logout_customer, name="customer_logout"),

    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),
    path('customer_order_details/<str:pk>', views.customer_order_details_page, name='customer_order_details'),
    path('customer_product_review/<str:pk>/<str:pk2>', views.customer_review, name='customer_product_review'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer_edit_profile/', views.customer_edit_profile, name='customer_edit_profile'),
    path('customer_reviews/', views.customer_reviews_page, name='customer_reviews'),
    path('customer_edit_review/<str:pk>/', views.customer_edit_review, name='customer_edit_review'),

    path('customer_reset_password/',
         auth_views.PasswordResetView.as_view(template_name='CustomerAndSalesManagement/customer_password_reset.html'),
         name='reset_password'),
    path('customer_reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='CustomerAndSalesManagement/customer_password_reset_sent.html'),
         name='password_reset_done'),
    path('customer_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='CustomerAndSalesManagement/customer_password_confirm.html'),
         name='password_reset_confirm'),
    path('customer_reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='CustomerAndSalesManagement/customer_password_reset_complete.html'),
         name='password_reset_complete'),

    path('cart/', views.cart, name="cart"),
    path('update_cart/', views.update_item, name="update_cart"),
    path('process_order/', views.process_order, name="process_order"),
    path('checkout/', views.checkout, name="checkout"),

    path('bulk_order_request/', views.bulk_order_request_page, name="bulk_order_request"),
    path('bulk_order_request_add_products/', views.bulk_order_request_add_products,
         name="bulk_order_request_add_products"),

    path('sales_dashboard/', views.sales_dashboard, name="CS_dashboard"),
    path('sales_products/', views.sales_product_page, name="sales_products"),
    path('create_product/', views.create_sales_products, name="create_product"),
    path('update_products/', views.update_product_page, name='update_products'),
    path('update_product/<str:pk>', views.update_sales_products, name='update_sales_products'),
    path('delete_product/<str:pk>', views.delete_sales_products, name='delete_sales_products'),

    path('sales_teams_management/', views.sales_teams_management, name='sales_teams_management'),
    path('manage_sales_teams/', views.manage_sales_teams, name='manage_sales_teams'),
    path('create_sales_team/', views.create_sales_team, name='create_sales_team'),
    path('update_sales_teams/', views.update_sales_teams, name='update_sales_teams'),
    path('assign_team_members/<str:pk>/<int:pk2>', views.assign_team_members, name='assign_team_members'),

    path('update_sales_teams_form/<str:pk>', views.update_sales_team_form, name='update_sales_team_form'),
    path(r'update_sales_team_members/(?P<pk>\d+)/$', views.update_sales_team_members, name='update_sales_team_members'),
    path('update_team_members/<str:pk>/<int:pk2>', views.update_team_members, name='update_team_members'),

    path('delete_sales_team/<str:pk>', views.delete_sales_team, name='delete_sales_team'),
    path('sales_team_information/<str:pk>', views.team_information_page, name='sales_team_information'),

    path('sales_tasks_management/', views.sales_tasks_management, name="sales_tasks_management"),
    path('create_sales_task/', views.create_sales_task, name='create_sales_task'),
    path('update_sales_tasks/', views.update_sales_tasks, name='update_sales_tasks'),
    path('update_sales_tasks_form/<str:pk>', views.update_sales_tasks_form, name='update_sales_tasks_form'),
    path('delete_sales_task/<str:pk>', views.delete_sales_task, name='delete_sales_task'),

    path('customer_management/', views.customer_management, name="customer_management"),
    path('customer_view/<str:pk>', views.view_customer, name="customer_view"),

    # Report Generation
    path('sales_products_pdf/', views.sales_products_pdf, name='sales_products_pdf'),
    path('sales_products_csv/', views.sales_products_csv, name='sales_products_csv'),
    path('sales_teams_csv/', views.sales_teams_csv, name='sales_teams_csv'),
    path('sales_task_csv/', views.sales_task_csv, name='sales_task_csv'),

]
