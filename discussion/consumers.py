import json
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from accounts.models import User
from discussion.models import Comment, Room, RoomUser, RoomBot, Theme, Bot, BotComment
from discussion.services import create_bot


def get_or_create_room(theme):

    if Room.objects.filter(theme=theme).exists():
        room = Room.objects.filter(theme=theme).last()
        
        if room.users.count() + room.bots.count() < 6:
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
             
        else:
            self.room.save()

            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            user = get_object_or_404(User, username=self.scope['user'])

            if not RoomUser.objects.filter(room=self.room, user=user).exists():
                RoomUser.objects.create(room=self.room, user=user)            

            self.accept()
            

    def disconnect(self, close_code):

        # self.room.bots.clear()

        if self.room.comments.count() == 0 or self.room.roomuser_set.count() == 0:
            self.room.delete()

        user = get_object_or_404(User, username=self.scope['user'])

        if Comment.objects.filter(room=self.room, author=user).count() == 0:
            self.room.roomuser_set.filter(user=user).delete()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        bot = text_data_json.get('bot')
        bot_comment = text_data_json.get('botComment')
        
        if not self.scope['user'].is_authenticated:
            return
        
        if message:
            color_value = text_data_json['colorValue']

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


        if bot:
            if Bot.objects.all().count() != 2:
                create_bot()

            bot_1 = Bot.objects.get(name='bot_1')
            bot_2 = Bot.objects.get(name='bot_2')

            if not RoomBot.objects.filter(room=self.room, bot=bot_1).exists():
                RoomBot.objects.create(room=self.room, bot=bot_1)  
            
            if not RoomBot.objects.filter(room=self.room, bot=bot_2).exists():
                RoomBot.objects.create(room=self.room, bot=bot_2)

        if bot_comment:
            random_comment = random.randint(0, 1)
            bot = Bot.objects.get(name=text_data_json.get('botName'))
            comment  = BotComment.objects.filter(bot=bot, color=text_data_json.get('botColor'))[random_comment]
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    'type': 'send_bot_comment',
                    'bot_name': bot.name,
                    'bot_comment': comment.comment,
                }
            )


    def discussion_message(self, event): 
        self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
        }))


    def send_room_users(self, event):
        self.send(text_data=json.dumps({
            'room_users': event['room_users'],
            'bots': event['bots']
        }))


    def send_bot_comment(self, event):
        self.send(text_data=json.dumps({
            'bot_name': event['bot_name'],
            'bot_comment': event['bot_comment']
        }))
