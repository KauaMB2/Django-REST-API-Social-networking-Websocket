from django.urls import re_path
from . import consumers

websocket_urlpatterns=[#Websocket url patterns list
	re_path(r'ws/socket-server/',consumers.ChatConsumer.as_asgi())#A websocket url
]
#path() function does not accept regex urls
#re_path() function just accept rexes urls 