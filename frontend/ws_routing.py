#  ===========================================================================================================
#  File Name: ws_routing.py
#  Description: This file contains url for Web Socket notifications on Client Dashboard.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

from django.urls import re_path,path
from . import ws_server

websocket_urlpatterns = [
    path('ws/notification/<str:user_id>', ws_server.Notification.as_asgi())
]