import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Order

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "admin_orders"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # 클라이언트로부터 메시지 수신 (필요 시 사용)
        pass

    async def order_notification(self, event):
        # 그룹으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))