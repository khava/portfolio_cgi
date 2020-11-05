from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core import serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from discussion.models import Room, RoomUser, RoomBot, Bot
from accounts.models import User


@receiver([post_save, post_delete], sender=RoomUser)
@receiver([post_save, post_delete], sender=RoomBot)
def room_users(sender, instance, **kwargs):
	
	room = Room.objects.get(name=instance.room)
	room_users = RoomUser.objects.filter(room=room)
	users = []
	
	for room_user in room_users:
		users.append(User.objects.get(username=room_user.user))

	room_bots = RoomBot.objects.filter(room=room)
	bots = []

	for room_bot in room_bots:
		bots.append(Bot.objects.get(name=room_bot.bot))
	
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		room.name,
		{
			'type': 'send_room_users',
			'room_users': serializers.serialize('json', users, fields=('username', 'avatar')),
			'bots': serializers.serialize('json', bots, fields=('name', 'avatar')),
		}
	)
