import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
#from apps.chat import routing
import apps.chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(apps.chat.routing.websocket_urlpatterns)
    )
})