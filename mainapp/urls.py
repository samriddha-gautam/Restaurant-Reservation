app_name = "mainapp"
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage view
    path('registration-success/', views.registration_success, name='registration_success'),
    
    # Customer-related paths
    path("register/", views.CustomerRegistrationView.as_view(), name="customer_register"),
    path('login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('profile/', views.UserProfileView.as_view(), name='userprofile_'),
    path('logout/', views.CustomerLogoutView, name='customer_logout'),
    path('add-reservation/', views.add_reservation, name='add_reservation'),
    path('reservation-success/', views.reservation_success, name='reservation_success'),

    # VIP-related paths
    path('vip-credentials',views.credentials_view,name='vip_credentials'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('set-credentials/', views.set_credentials_view, name='set_credentials'),
    path('vip-login/', views.VIPCustomerLoginView.as_view(), name='vip_customer_login'),
    path('vip-profile/', views.VIPUserProfileView.as_view(), name='vip_userprofile_'),
    path('vip-reservation/', views.add_vip_reservation, name='vip_reservation'),
    path('vip-reservation-success/', views.vip_reservation_success, name='vip_reservation_success'),
    path('vip-logout/', views.VIPCustomerLogoutView, name='vip_customer_logout'),
]
