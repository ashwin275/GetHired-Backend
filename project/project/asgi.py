import os

from channels.auth import AuthMiddlewareStack  #type:ignore
from channels.routing import ProtocolTypeRouter, URLRouter  #type:ignore
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django_asgi_app = get_asgi_application()

import chat.routing


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket":
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))

    }
)
