import json
import os
import threading

from discussion.models import Bot, BotComment, RoomBot


def create_bot():

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
			create_bot()

		bot_1 = Bot.objects.get(name='bot_1')
		bot_2 = Bot.objects.get(name='bot_2')

		if not RoomBot.objects.filter(room=room, bot=bot_1).exists():
			RoomBot.objects.create(room=room, bot=bot_1)  
		
		if not RoomBot.objects.filter(room=room, bot=bot_2).exists():
			RoomBot.objects.create(room=room, bot=bot_2)
	
	if bot == 'bot_1':
		if Bot.objects.all().count() != 2:
			create_bot()

		bot_1 = Bot.objects.get(name='bot_1')

		if not RoomBot.objects.filter(room=room, bot=bot_1).exists():
			RoomBot.objects.create(room=room, bot=bot_1)


def setInterval(interval, times = -1):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()

            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap
