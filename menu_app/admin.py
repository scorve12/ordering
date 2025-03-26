# admin.py
from django.contrib import admin
from .models import Table, MenuItem, Order, OrderItem

admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)