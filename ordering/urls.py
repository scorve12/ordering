# ordering/urls.py
from django.contrib import admin
from django.urls import path
from menu_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.menu_list, name='menu_list'),  # 루트 URL에 메뉴 리스트 연결
    path('qr/<int:table_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('order/<int:table_id>/', views.order_page, name='order_page'),
    path('order/<int:table_id>/submit/', views.submit_order, name='submit_order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]