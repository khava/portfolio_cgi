import json
from builtins import object

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core import serializers

from accounts.models import User
from discussion.models import Comment, Room, RoomUser, Theme


def get_or_create_room(theme):

    if Room.objects.filter(theme=theme).exists():
        room = Room.objects.filter(theme=theme).last()
        
        if room.users.count() < 6:
            room_name = room.name
        else:
            room_name = f'theme_{theme.pk}_room_{room.pk + 1}'
            room = Room()
            room.name = room_name
            room.theme = theme
    else:
        room_name = f'theme_{theme.pk}_room_1'
        room = Room()
        room.name = room_name
        room.theme = theme

    return room, room_name
    

class DiscussionConsumer(WebsocketConsumer):

    def connect(self):

        self.theme = Theme.objects.filter(pk=self.scope['url_route']['kwargs']['theme_id']).first()
        self.room, self.room_name = get_or_create_room(self.theme)

        if self.scope['user'].is_anonymous or self.theme.author == self.scope['user']:
            self.close()

            print('CONNECT CLOSE')
             
        else:
            self.room.save()

            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            user = User.objects.get(username=self.scope['user'])

            if not RoomUser.objects.filter(room=self.room, user=user).exists():
                RoomUser.objects.create(room=self.room, user=user)            

            self.accept()
            
            print('CONNECT')


    def disconnect(self, close_code):

        print('DISCONNECT')

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )


    def receive(self, text_data):
        print('RECEIVE')

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        color_value = text_data_json['colorValue']
        
        if not message or not self.scope['user'].is_authenticated:
            return

        if len(message) > 10:

            Comment.objects.create(
                comment=message,
                color=color_value,
                theme=self.theme,
                author=User.objects.get(username=self.scope['user']),
                room=self.room,
            )


        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'discussion_message',
                'message': message,
                'user': str(self.scope['user']),
            }
        )


    def discussion_message(self, event):
        print('DISCUSSION_MESSAGE')
        
        self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
        }))



# class RoomUsersDisplayConsumer(WebsocketConsumer):

    # def connect(self):

    #     self.theme = Theme.objects.filter(pk=self.scope['url_route']['kwargs']['theme_id']).first()
    #     self.room, self.room_name = get_or_create_room(self.theme)

    #     async_to_sync(self.channel_layer.group_add)(
    #         self.room_name,
    #         self.channel_name
    #     )
        
    #     self.accept()

    #     self.is_connected = True

    #     while self.is_connected:

    #         room_users = serializers.serialize('json', self.room.users.all())
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.room_name,
    #             {
    #                 'type': 'send_room_users',
    #                 'room_users': room_users,
    #             }
    #         )
            
    # def disconnect(self, close_code):

    #     self.is_connected = False

    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_name,
    #         self.channel_name
    #     )

    # def send_room_users(self, event):

    #     print(event)
        
    #     self.send(text_data=json.dumps({
    #         'room_users': event['room_users'],
    #     }))
