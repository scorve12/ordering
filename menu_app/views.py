from django.shortcuts import render
from .models import MenuItem, Order, OrderItem, Table
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def menu_view(request):
    table_id = request.GET.get('table')
    table = Table.objects.get(id=table_id) if table_id else None
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        selected_items = request.POST.getlist('items')
        quantities = request.POST.getlist('quantity')
        total_price = 0
        order = Order.objects.create(table=table, total_price=0)
        for item_id, qty in zip(selected_items, quantities):
            if int(qty) > 0:
                menu_item = MenuItem.objects.get(id=item_id)
                total_price += menu_item.price * int(qty)
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=qty)
        order.total_price = total_price
        order.save()

        # WebSocket으로 알림 전송
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "admin_orders",
            {
                "type": "order_notification",
                "message": f"New order from {table.name}: {total_price}원"
            }
        )
        return render(request, 'menu_app/order_success.html')
    return render(request, 'menu_app/menu.html', {'menu_items': menu_items, 'table': table})

def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'menu_app/admin_orders.html', {'orders': orders})