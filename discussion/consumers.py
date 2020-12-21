import json
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from accounts.models import User
from discussion.models import Comment, Room, RoomUser, RoomBot, Theme, Bot, BotComment


class BaseDiscussionConsumer(WebsocketConsumer):

    def connect(self):

        self.theme = Theme.objects.filter(pk=self.scope['url_route']['kwargs']['theme_id']).first()
        self.user = get_object_or_404(User, username=self.scope['user'])
        
        if self.scope['user'].is_anonymous or self.theme.author == self.user.username:
            self.close()

        else:
            if not Room.objects.filter(theme=self.theme).exists():
                room_name = f'theme_{self.theme.pk}_room_1'
                print(room_name)
                self.room = Room.objects.create(name=room_name, theme=self.theme)
            
            elif self.user.rooms.filter(theme=self.theme, closed=False).exists():
                self.room = self.user.rooms.filter(theme=self.theme, closed=False).last()
                print('users', self.room)

            elif Room.objects.filter(theme=self.theme, closed=False).exists():
                self.room = Room.objects.filter(theme=self.theme, closed=False).last()
                print('room', self.room)
                
                if self.room.users.count() + self.room.bots.count() >= 6:
                    room_name = f'theme_{self.theme.pk}_room_{self.room.pk + 1}'
                    print('1',room_name)
                    self.room = Room.objects.create(name=room_name, theme=self.theme)
                    print('room >6', self.room)
            else:
                self.room = Room.objects.filter(theme=self.theme).last()
                room_name = f'theme_{self.theme.pk}_room_{self.room.pk + 1}'
                self.room = Room.objects.create(name=room_name, theme=self.theme)
                print('room treu', self.room)

            async_to_sync(self.channel_layer.group_add)(
                self.room.name,
                self.channel_name
            )
            
            if not RoomUser.objects.filter(room=self.room, user=self.user).exists():
                RoomUser.objects.create(room=self.room, user=self.user)            

            self.accept()


    def disconnect(self, close_code):

        if self.room.roomuser_set.count() <= 4 and not self.room.closed:
            self.room.bots.clear()

        if Comment.objects.filter(room=self.room, author=self.user).count() == 0 and not self.room.closed:
            self.room.roomuser_set.filter(user=self.user).delete()

        if self.room.comments.count() == 0 and self.room.roomuser_set.count() < 1:
            self.room.delete()

        async_to_sync(self.channel_layer.group_discard)(
            self.room.name,
            self.channel_name
        )

    
class DiscussionConsumer(BaseDiscussionConsumer, WebsocketConsumer):

    def connect(self):
        return super().connect()

    def disconnect(self, close_code):
        return super().disconnect(close_code)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        bot_comment = text_data_json.get('botComment')
        closed = text_data_json.get('closed')
        

        if not self.scope['user'].is_authenticated:
            return

        if closed:
            self.room.closed = True
            self.room.save()
        
        if message:
            color_value = text_data_json.get('colorValue')

            if len(message) > 10:
                Comment.objects.create(comment=message, color=color_value, theme=self.theme, author=self.user, room=self.room)

            async_to_sync(self.channel_layer.group_send)(
                self.room.name,
                {
                    'type': 'send_discussion_message',
                    'message': message,
                    'user': str(self.scope['user']),
                }
            )

        if bot_comment:
            bot_name = text_data_json.get('botName')
            bot_color = text_data_json.get('botColor')
            random_comment = random.randint(0, 1)

            bot = Bot.objects.get(name=bot_name)
            try:
                comment  = BotComment.objects.filter(bot=bot, color=bot_color)[random_comment]
                
                async_to_sync(self.channel_layer.group_send)(
                    self.room.name,
                    {
                        'type': 'send_bot_comment',
                        'bot_name': bot.name,
                        'bot_comment': comment.comment,
                    }
                )
            except IndexError:
                pass


    def send_discussion_message(self, event): 
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

    def send_colors(self, event):
        self.send(text_data=json.dumps({
            'colors': event['colors'],
            'color_description': event['color_description']
        }))
