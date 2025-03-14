from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('reservations/', views.dashboard_reservations, name='dashboard_reservations'),
    path('meals/', views.dashboard_meals, name='dashboard_meals'),
    path('users/', views.dashboard_users, name='dashboard_users'),
    path('reservations/modify/<int:reservation_id>/', views.modify_reservation, name='modify_reservation'),
    path('reservations/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]