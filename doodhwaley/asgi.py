"""
ASGI config for doodhwaley project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# doodhwaley/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import milkapp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doodhwaley.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            milkapp.routing.websocket_urlpatterns
        )
    ),
})