from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page_1, name="landing_page_1"),
    path('', include('CustomerAndSalesManagement.urls')),
    path('login/', views.loginuser, name="user-login"),
    path('logout/', views.logoutuser, name="user-logout"),
    # Profile URLs
    path('profile/', views.profile, name="wm-profile"),
    path('profile/password/change/',
         auth_views.PasswordChangeView.as_view
         (template_name='Users/passwordchange.html',
          success_url='/warehouse/dashboard/'),
         name="wm-profile-password-change"),
    path('supplierlogin/', views.slogin, name="user-slogin"),
]
