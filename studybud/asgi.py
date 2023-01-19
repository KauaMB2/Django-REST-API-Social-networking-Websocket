"""
ASGI config for studybud project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import base.routing

#The channels's routing configuration said what kind of code must be run when receive a HTTP request by a channel server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')#Set where is the settings file in the project

application = ProtocolTypeRouter({#List of protocols in our application and what kind of code must according each protocol
	'http':get_asgi_application(),#What code run in a HTTP request...
	'websocket':AuthMiddlewareStack(URLRouter(base.routing.websocket_urlpatterns))#Pass all the URLs listed in "websocket_urlpatterns"
	})

