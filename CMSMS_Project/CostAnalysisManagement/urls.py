from django.urls import path
from . import views


urlpatterns = [
    path('CA_dashboard/', views.CA_dashboard, name="CA_dashboard"),
    path('mess/', views.messages, name="messages"),


    path('products/', views.CA_dashboard, name="CA-products"),


    path('index/', views.index, name="index"),
    path('add-expenses/', views.add_expense, name="add-expenses"),
    path('update-expense/<str:pk>/', views.update_expenses, name="update-expense"),
    path('delete-expense/<str:pk>/', views.delete_expeses, name="delete-expense"),

    path('income/', views.income, name="income"),
    path('add-income/', views.add_income, name="add-income"),
    path('update-income/<str:pk>/', views.update_income, name="update-income"),
    path('delete-income/<str:pk>/', views.delete_income, name="delete-income"),


    path('production-cost/', views.production_cost, name="production-cost"),
    path('add-procost/', views.add_proCost, name="add-procost"),
    path('update-procost/<str:pk>/', views.update_production_cost, name="update-procost"),
    path('delete-procost/<str:pk>/', views.delete_production_cost, name="delete-procost"),


    path('directmaterial-cost/', views.directmaterial_cost, name="directmaterial-cost"),
    path('add-dmcost/', views.add_directmaterial_cost, name="add-directmaterial-cost"),
    path('update-dmcost/<str:pk>/', views.update_directmaterial_cost, name="update-directmaterial-cost"),
    path('delete-dmcost/<str:pk>/', views.delete_directmaterial_cost, name="delete-directmaterial-cost"),


    path('directlabor-cost/', views.directlabor_cost, name="directlabor-cost"),
    path('add-dlcost/', views.add_directlabor_cost, name="add-directlabor-cost"),
    path('update-dlcost/<str:pk>/', views.update_directlabor_cost, name="update-directlabor-cost"),
    path('delete-dlcost/<str:pk>/', views.delete_directlabor_cost, name="delete-directlabor-cost"),


    path('factoryoverheads-cost/', views.factory_overheads_cost, name="factoryoverheads-cost"),
    path('add-focost/', views.add_factory_overheads_cost, name="add-factoryoverheads-cost"),
    path('update-focost/<str:pk>/', views.update_factory_overheads_cost, name="update-factoryoverheads-cost"),
    path('delete-focost/<str:pk>/', views.delete_factory_overheads_cost, name="delete-factoryoverheads-cost"),


    path('retail-price/', views.retail_price, name="retail-price"),
    path('add-raprice/', views.add_retail_price, name="add-retail-price"),
    path('update-reprice<str:pk>/', views.update_retail_price, name="update-reprice"),
    path('delete-reprice<str:pk>/', views.delete_retail_price, name="delete-reprice"),

    path('CA-profile/', views.profile, name="CA-profile"),

    path('exreport/', views.expensesCSV, name="exreport"),
    path('pcreport/', views.productionCostCSV, name="pcreport"),
    path('dmreport/', views.directMaterialCostCSV, name="dmreport"),
    path('dlreport/', views.directLaborCostCSV, name="dlreport"),
    path('foreport/', views.factoryOverheadsCSV, name="foreport"),
    path('inreport/', views.incomeCSV, name="inreport"),
    path('rxreport/', views.retailCSV, name="rxreport"),

]
