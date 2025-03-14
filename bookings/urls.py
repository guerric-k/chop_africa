from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu_view, name='menu'),
    path('contact/', views.contact_view, name='contact'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('reservations/', views.view_reservations, name='view_reservations'),
    path('reservations/modify/<int:reservation_id>/', views.modify_reservation, name='modify_reservation'),
    path('reservations/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]