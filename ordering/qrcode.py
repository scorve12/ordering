import qrcode
from django.conf import settings

def generate_qr_codes():
    tables = Table.objects.all()
    for table in tables:
        url = f"http://localhost:8000/menu?table={table.id}"  # 배포 시 도메인으로 변경
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f"qr_table_{table.id}.png")

# 실행 예: Python shell에서
# from menu_app.models import Table
# from your_script import generate_qr_codes
# generate_qr_codes()