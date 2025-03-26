import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import menu_app.routing  # 나중에 추가할 routing 모듈

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            menu_app.routing.websocket_urlpatterns
        )
    ),
})