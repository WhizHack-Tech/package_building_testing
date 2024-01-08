"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

#  ==============================================================================================================================================================================================================================================================================================================================
#  File Name: asgi.py
#  Description: Automatically generated file and included by default in Django project. This file is used to configure and run the ASGI (Asynchronous Server Gateway Interface) application, which is necessary for handling asynchronous tasks, WebSocket connections, and real-time functionality in Django applications.

#  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===============================================================================================================================================================================================================================================================================================================================

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import frontend.ws_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            frontend.ws_routing.websocket_urlpatterns
        )
    )
})