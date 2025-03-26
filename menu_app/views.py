# views.py
import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from decimal import Decimal
from .models import MenuItem, Table, Order, OrderItem

def generate_qr_code(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    qr_url = f"http://127.0.0.1:8000/order/{table.id}/"  # QR 코드에 포함될 URL
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill='black', back_color='white')
    response = HttpResponse(content_type="image/png")
    qr_image.save(response, "PNG")
    return response

def menu_list(request):
    menu_items = MenuItem.objects.all()  # 모든 메뉴 아이템 가져오기
    return render(request, 'menu_list.html', {'menu_items': menu_items})

def order_page(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    menu_items = MenuItem.objects.all()

    # 세션에서 장바구니 가져오기 (없으면 빈 리스트)
    cart = request.session.get('cart', {})

    # "담기" 요청 처리
    if request.method == 'POST' and 'add_to_cart' in request.POST:
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        if menu_item_id:
            # 장바구니에 추가 (메뉴 ID와 수량 저장)
            if menu_item_id in cart:
                cart[menu_item_id] += quantity
            else:
                cart[menu_item_id] = quantity
            request.session['cart'] = cart
            return redirect('order_page', table_id=table_id)

    # 장바구니에 담긴 메뉴 정보 가져오기
    cart_items = []
    total_price = Decimal('0.00')
    for item_id, qty in cart.items():
        item = MenuItem.objects.get(id=item_id)
        item_total = item.price * qty
        cart_items.append({'item': item, 'quantity': qty, 'total': item_total})
        total_price += item_total

    return render(request, 'order_page.html', {
        'table': table,
        'menu_items': menu_items,
        'cart_items': cart_items,
        'total_price': total_price,
    })

def submit_order(request, table_id):
    if request.method == 'POST':
        table = get_object_or_404(Table, id=table_id)
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('order_page', table_id=table_id)

        # 주문 생성
        order = Order.objects.create(table=table, total_price=Decimal('0.00'))
        total_price = Decimal('0.00')

        # 장바구니 아이템 추가
        for item_id, qty in cart.items():
            menu_item = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=qty)
            total_price += menu_item.price * qty

        order.total_price = total_price
        order.save()

        # 세션 장바구니 비우기
        request.session['cart'] = {}
        return redirect('order_confirmation', order_id=order.id)
    return redirect('order_page', table_id=table_id)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})