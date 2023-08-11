import os

from channels.auth import AuthMiddlewareStack  #type:ignore
from channels.routing import ProtocolTypeRouter, URLRouter  #type:ignore
from channels.security.websocket import AllowedHostsOriginValidator  #type:ignore
from django.core.asgi import get_asgi_application

from chat.routing import websocket_urlpatterns
from chat.middleware import TokenAuthMiddleware
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": 
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
       
    }
)