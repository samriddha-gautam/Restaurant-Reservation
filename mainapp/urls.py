app_name="mainapp"
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Simple website view
    # path('dashboard/', views.dashboard, name='dashboard'), 
    path("register/",views.CustomerRegistrationView.as_view(), name="home"),
    path('registration-success/', views.registration_success, name='registration_success'),  # Optional staff dashboard view
    path('login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('profile/', views.UserProfileView.as_view(), name='userprofile_'),
    path('logout/', views.CustomerLogoutView, name='customer_logout'),
    path('add-reservation/',views.add_reservation,name='add_reservation'),
    path('reservation-success/',views.reservation_success,name='reservation_success'),
    path('credentials/', views.credentials_view, name='credentials'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('vip-reservation/',views.vip_reservation_view,name='vip_reservation'),
    # path('home/',views.homepage,name="home"),
]