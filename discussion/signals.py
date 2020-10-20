from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core import serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from discussion.models import Room, RoomUser
from accounts.models import User


@receiver([post_save, post_delete], sender=RoomUser)
def room_users(sender, instance, **kwargs):
	room_name = str(instance).split()[0]
	room = Room.objects.get(name=room_name)
	room_users = RoomUser.objects.filter(room=room)
	users = []
	for room_user in room_users:
		users.append(User.objects.get(username=room_user.user))

	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		room_name,
		{
			'type': 'send_room_users',
			'room_users': serializers.serialize('json', users, fields=('username', 'avatar')),
		}
	)
