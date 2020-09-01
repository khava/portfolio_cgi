import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from discussion.models import Theme, Comment
from accounts.models import User


class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # print(len(Group('guis').channel_layer.group_channels('guis')))
        print(len(self.channel_layer.groups.get(self.room_name, {}).items()))

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        
        if self.scope["user"].is_anonymous or Theme.objects.filter(pk=self.room_name).first().author == self.scope['user']:
            self.send()
            self.close()
        else:
            self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = str(self.scope['user'])
        
        if not message:
            return
        if not self.scope['user'].is_authenticated:
            return

        if len(message) > 10:

            Comment.objects.create(
                author=User.objects.get(username=user),
                comment=message,
                theme=Theme.objects.get(pk=self.room_name),
                color='yellow' # !!!
            )

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        
        self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))