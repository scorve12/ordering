# menu_app/populate_test_data.py
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ordering.settings')
django.setup()

from menu_app.models import Table, MenuItem, Order, OrderItem

def populate_test_data():
    Table.objects.all().delete()
    MenuItem.objects.all().delete()
    Order.objects.all().delete()
    OrderItem.objects.all().delete()

    tables = [
        Table(name="1"),
        Table(name="2"),
        Table(name="3"),
    ]
    Table.objects.bulk_create(tables)
    print("테이블 데이터 생성 완료")

    menu_items = [
        {"name": "김치찌개", "description": "맛있는 김치찌개", "price": Decimal('8000.00'), "category": "한식"},
        {"name": "불고기", "description": "달콤한 불고기", "price": Decimal('9000.00'), "category": "한식"},
        {"name": "파스타", "description": "크림 파스타", "price": Decimal('7000.00'), "category": "양식"},
        {"name": "피자", "description": "치즈 피자", "price": Decimal('9500.00'), "category": "양식"},
    ]
    for item in menu_items:
        MenuItem.objects.create(**item)
    print("메뉴 아이템 데이터 생성 완료")

    table1 = Table.objects.get(name="1")
    table2 = Table.objects.get(name="2")
    
    order1 = Order.objects.create(table=table1, total_price=Decimal('0.00'), status="pending")
    order2 = Order.objects.create(table=table2, total_price=Decimal('0.00'), status="completed")

    menu1 = MenuItem.objects.get(name="김치찌개")
    menu2 = MenuItem.objects.get(name="피자")
    menu3 = MenuItem.objects.get(name="불고기")

    OrderItem.objects.create(order=order1, menu_item=menu1, quantity=2)
    OrderItem.objects.create(order=order1, menu_item=menu2, quantity=1)
    order1.total_price = (menu1.price * 2) + menu2.price
    order1.save()

    OrderItem.objects.create(order=order2, menu_item=menu3, quantity=1)
    order2.total_price = menu3.price
    order2.save()
    print("주문 및 주문 아이템 데이터 생성 완료")

if __name__ == "__main__":
    print("테스트 데이터 생성 시작...")
    populate_test_data()
    print("테스트 데이터 생성 완료!")