from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return
        else:
            self.GROUP_NAME = self.user.notification_group_name
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.GROUP_NAME, self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
            )
            self.close()

    def user_followed(self, event):

        # self.send(text_data=f'{event["username"]} followed you')

        html = get_template('partials/notification.html').render(
            context={'username': event['username']})

        self.send(text_data=html)