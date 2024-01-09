#  ===========================================================================================================
#  File Name: ws_server.py
#  Description: This file contains code for Web Socket notifications on Client Dashboard.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

import json
import logging

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from .ws_query_helper import _main


class Notification(WebsocketConsumer):
    def connect(self):
        # Get user ID from URL
        user_id = self.scope["url_route"]["kwargs"]["user_id"]

        self.room_group_name = user_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        try:
            if self.room_group_name and self.channel_layer.groups:
                if self.channel_layer.groups.get(self.room_group_name, None):
                    async_to_sync(self.channel_layer.group_discard)(
                        self.room_group_name,
                        list(self.channel_layer.groups[self.room_group_name].keys())[0],
                    )
            logging.info(f"WebSocket disconnected with close code: {close_code}")
            self.close()

        except StopConsumer:
            pass

        except Exception as e:
            logging.exception(f"Unexpected error during disconnect: {e}")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        email_id = str(text_data_json.get("email"))

        if email_id != "None":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": _main(email_id)},
            )
        else:
            pass

    def chat_message(self, event):
        message = event["message"]

        try:
            self.send(text_data=json.dumps({"type": "chat", "message": message}))
        except Exception:
            self.close()
