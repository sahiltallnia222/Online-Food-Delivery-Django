
from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register',views.registerUser,name='registerUser'),
    path('register-vendor',views.registerVendor,name='registerVendor'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('myAccount',views.myAccount,name='myAccount'),
    path('custDashboard',views.custDashboard,name='custDashboard'),
    path('vendorDashboard',views.vendorDashboard,name='vendorDashboard'),
]