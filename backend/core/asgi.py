"""
ASGI config for settings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.core.asgi import get_asgi_application  # noqa E:402
from channels.routing import ProtocolTypeRouter, URLRouter # noqa E:402

import core.routing# noqa E:402
from core.middleware import JWTAuthMiddlewareStack# noqa E:402

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        JWTAuthMiddlewareStack(
            URLRouter(core.routing.websocket_urlpatterns))
})
