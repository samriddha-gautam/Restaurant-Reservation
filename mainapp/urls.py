from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Simple website view
    path('dashboard/', views.dashboard, name='dashboard'),  # Optional staff dashboard view
    path('add-reservation/',views.add_reservation,name='add_reservation'),
    path('reservation-success/',views.reservation_success,name='reservation_success'),
]