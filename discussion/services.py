import json
import os
import threading

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from discussion.models import Room, RoomUser, RoomBot, Bot
from discussion.models import Bot, BotComment, RoomBot


MAX_NUMBER_PARTICIPANTS = 6
ONE_PARTICIPANTS_TIME = 60.0
COLORS = 'blue, white, red, black, yellow, green'
COLOR_DESCRIPTION = 'Управление, Информация и факты, Эмоции и Чувства, Критическое суждение, Оптимистичность, Креативность'


def create_bots():

    data_path = os.path.join(os.path.dirname(__file__), 'data.json')

    bot_1, _ = Bot.objects.get_or_create(name='bot_1')
    bot_2, _ = Bot.objects.get_or_create(name='bot_2')

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for color in data:
        for comment in data[color]:
            BotComment.objects.get_or_create(comment=comment, color=color, bot=bot_1)
            BotComment.objects.get_or_create(comment=comment, color=color, bot=bot_2)


def add_bots_to_room(bot, room):	
	
	if bot == 'bots':
		if Bot.objects.all().count() != 2:
			create_bots()

		bot_1 = Bot.objects.get(name='bot_1')
		bot_2 = Bot.objects.get(name='bot_2')

		if not RoomBot.objects.filter(room=room, bot=bot_1).exists():
			RoomBot.objects.create(room=room, bot=bot_1)  
		
		if not RoomBot.objects.filter(room=room, bot=bot_2).exists():
			RoomBot.objects.create(room=room, bot=bot_2)
	
	if bot == 'bot_1':
		if Bot.objects.all().count() != 2:
			create_bots()

		bot_1 = Bot.objects.get(name='bot_1')

		if not RoomBot.objects.filter(room=room, bot=bot_1).exists():
			RoomBot.objects.create(room=room, bot=bot_1)


def add_bots(room):
	room_users = RoomUser.objects.filter(room=room)
	
	if room_users.count() == 4:
		print('### Add TWO bots to room ###')
		add_bots_to_room('bots', room)

	if room_users.count() == 5:
		print('### Add ONE bot to room ###')
		add_bots_to_room('bot_1', room)


def setInterval(interval, times = -1):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()

            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    if stop.isSet() is False:
                        function(*args, **kwargs)
                        i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap


def send_colors(room, colors_list, color_description_list):
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		room,
		{
			'type': 'send_colors',
			'colors': json.dumps(colors_list),
			'color_description': json.dumps(color_description_list),
		}
	)
    

def permutation_color(room):

	colors_list = room.colors.split(', ')
	color_description_list = room.color_description.split(', ')

	colors_list.insert(0, colors_list.pop())
	color_description_list.insert(0, color_description_list.pop())

	room.colors = ', '.join(colors_list)
	room.color_description = ', '.join(color_description_list)
	room.save(update_fields=['colors', 'color_description'])

	colors_list = room.colors.split(', ')
	color_description_list = room.color_description.split(', ')
	print(f'### IN Permutation color - {colors_list} ###')
	send_colors(room.name, colors_list, color_description_list)

	if colors_list[-1] == 'blue':
		room.colors = COLORS
		room.color_description = COLOR_DESCRIPTION
		room.save(update_fields=['colors', 'color_description'])


def change_color(room):
	room_users = RoomUser.objects.filter(room=room)
	room_bots = RoomBot.objects.filter(room=room)

	if room_users.count() == MAX_NUMBER_PARTICIPANTS or room_users.count() + room_bots.count() == MAX_NUMBER_PARTICIPANTS:		
		colors_list = room.colors.split(', ')
		color_description_list = room.color_description.split(', ')
		print(f'### OUT Permutation color - {colors_list} ###')
		send_colors(room.name, colors_list, color_description_list)
 
		color_permutation_times = 6 - (colors_list.index('blue') + 1)
		p_color = setInterval(ONE_PARTICIPANTS_TIME, color_permutation_times)(permutation_color)
		p_color(room)
