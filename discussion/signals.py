import json
from threading import Timer

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core import serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from accounts.models import User
from discussion.models import Room, RoomUser, RoomBot, Bot
from discussion.services import setInterval, add_bots_to_room


colors = ['blue', 'white', 'red', 'black', 'yellow', 'green']
color_description = ['Управление', 'Информация и факты', 'Эмоции и Чувства', 'Критическое суждение', 'Оптимистичность', 'Креативность']

MAX_NUMBER_PARTICIPANTS = 6
ONE_PARTICIPANTS_TIME = 60.0

bot_add_timer = None
change_color_timer = None
stop_change_color = False


@receiver([post_save, post_delete], sender=RoomUser)
@receiver([post_save, post_delete], sender=RoomBot)
def room_users(sender, instance, **kwargs):
	
	room = Room.objects.get(name=instance.room)

	room_users = RoomUser.objects.filter(room=room)	
	users = [User.objects.get(username=room_user.user) for room_user in room_users]

	room_bots = RoomBot.objects.filter(room=room)
	bots = [Bot.objects.get(name=room_bot.bot) for room_bot in room_bots]

	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		room.name,
		{
			'type': 'send_room_users',
			'room_users': serializers.serialize('json', users, fields=('username', 'avatar')),
			'bots': serializers.serialize('json', bots, fields=('name', 'avatar')),
		}
	)


@receiver([post_save, post_delete], sender=RoomUser)
def room_bots(sender, instance, **kwargs):
	room = Room.objects.get(name=instance.room)
	room_users = RoomUser.objects.filter(room=room)
	
	global bot_add_timer

	if room_users.count() == 4:
		if bot_add_timer is not None: bot_add_timer.cancel()
		print('### Add TWO bots to room ###')
		bot_add_timer = Timer(15.0, add_bots_to_room, ('bots', room))
		bot_add_timer.start()

	elif room_users.count() == 5:
		print('### Add ONE bot to room ###')
		if bot_add_timer is not None: bot_add_timer.cancel()
		bot_add_timer = Timer(15.0, add_bots_to_room, ('bot_1', room))
		bot_add_timer.start()


def permutation_color(room):

	global colors
	global color_description
	global stop_change_color

	print(f'### Permutation color - {colors} ###')

	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		room.name,
		{
			'type': 'send_colors',
			'colors': json.dumps(colors),
			'color_description': json.dumps(color_description),
		}
	)

	if colors[-1] == 'blue':
		colors = ['blue', 'white', 'red', 'black', 'yellow', 'green'];
		color_description = ['Управление', 'Информация и факты', 'Эмоции и Чувства', 'Критическое суждение', 'Оптимистичность', 'Креативность'];
		stop_change_color = True
		return

	colors.insert(0, colors.pop())
	color_description.insert(0, color_description.pop())


@receiver([post_save, post_delete], sender=RoomUser)
@receiver([post_save, post_delete], sender=RoomBot)
def change_color(sender, instance, **kwargs):
	room = Room.objects.get(name=instance.room)
	room_users = RoomUser.objects.filter(room=room)
	room_bots = RoomBot.objects.filter(room=room)

	global change_color_timer
	global colors
	global color_description

	if room_users.count() == MAX_NUMBER_PARTICIPANTS or room_users.count() + room_bots.count() == MAX_NUMBER_PARTICIPANTS:
		print('### Colors change started ###')

		permutation_color(room)
		p_color = setInterval(ONE_PARTICIPANTS_TIME, 5)(permutation_color)
		change_color_timer = p_color(room)
			
	if change_color_timer is not None and room_users.count() < MAX_NUMBER_PARTICIPANTS and room_users.count() + room_bots.count() < MAX_NUMBER_PARTICIPANTS:
		print('### Colors change stoped, because participtnts < 6 ###')
		
		colors = ['blue', 'white', 'red', 'black', 'yellow', 'green']
		color_description = ['Управление', 'Информация и факты', 'Эмоции и Чувства', 'Критическое суждение', 'Оптимистичность', 'Креативность']
		print(colors)
		change_color_timer.set()

	if stop_change_color is True and change_color_timer is not None:
		print('### Colors change stoped, change color is successful ###')
		
		colors = ['blue', 'white', 'red', 'black', 'yellow', 'green']
		color_description = ['Управление', 'Информация и факты', 'Эмоции и Чувства', 'Критическое суждение', 'Оптимистичность', 'Креативность']
		print(colors)
		change_color_timer.set()
		





	

	


		


	
