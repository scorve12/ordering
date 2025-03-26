from django.urls import path
from menu_app import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
]