import json
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from accounts.models import User
from discussion.models import Comment, Room, RoomUser, RoomBot, Theme, Bot, BotComment
from discussion.services import change_color, add_bots, send_colors


class DiscussionConsumer(WebsocketConsumer):

    def connect(self):

        self.room = get_object_or_404(Room, pk=self.scope['url_route']['kwargs']['room_id'])
        self.theme = self.room.theme
        self.user = get_object_or_404(User, username=self.scope['user'])
        
        if self.scope['user'].is_anonymous or self.theme.author == self.user.username:
            self.close()

        async_to_sync(self.channel_layer.group_add)(
            self.room.name,
            self.channel_name
        )

        if self.room.users.count() < 6:
            if not RoomUser.objects.filter(room=self.room, user=self.user).exists():
                RoomUser.objects.create(room=self.room, user=self.user)            
        
        self.accept()

        if self.room.started and not self.room.closed:
            change_color(self.room)
            

    def disconnect(self, close_code):

        if self.room.roomuser_set.count() < 4:
            self.room.bots.clear()

        if self.room.roomuser_set.count() < 1:
            self.room.delete()

        async_to_sync(self.channel_layer.group_discard)(
            self.room.name,
            self.channel_name
        )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        color_value = text_data_json.get('colorValue')
        is_user_leave_room = text_data_json.get('isUserLeaveRoom')
        is_discussion_start = text_data_json.get('isDiscussionStart')
        is_bots_add = text_data_json.get('isBotsAdd')
        is_get_bot_comment = text_data_json.get('isGetBotComment')
        is_closed = text_data_json.get('closed')

        if is_user_leave_room:
            self.room.roomuser_set.filter(user=self.user).delete()

        if is_discussion_start:
            self.room.started = True
            self.room.save(update_fields=['started'])
            change_color(self.room)

        if message: 
            if color_value:
                Comment.objects.create(comment=message, color=color_value, theme=self.theme, author=self.user, room=self.room)

            async_to_sync(self.channel_layer.group_send)(
                self.room.name,
                {
                    'type': 'send_discussion_message',
                    'message': message,
                    'user': str(self.scope['user']),
                }
            )
        
        if is_bots_add:
            add_bots(self.room)

        if is_get_bot_comment:
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

        if is_closed:
            self.room.closed = True
            self.room.save(update_fields=['closed'])



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


class NumberParticipantsRoomDisplayConsumer(WebsocketConsumer):

    def connect(self):

        if not self.scope['user'].is_authenticated:
            self.close

        self.room_name = 'number_participants'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
            
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def send_num_participants(self, event):
        self.send(text_data=json.dumps({
            'num_participants': event['num_participants'],
        }))
