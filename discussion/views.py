from itertools import chain

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from discussion.models import Theme, Room, RoomUser, Comment
from accounts.models import User
from discussion.forms import CreateThemeForm


class DisplayThemesView(ListView):
    model = Theme
    context_object_name = 'themes'
    template_name = 'discussion/theme_list.html'


class CreateThemeView(CreateView):

    @method_decorator(login_required)
    def get(self, request):
        form = CreateThemeForm()
        return render(request, 'discussion/theme_create.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = CreateThemeForm(request.POST)

        if form.is_valid():
            theme = form.save(commit=False)
            theme.author = request.user
            theme.save()

        return redirect(reverse('main_page'))

    
class DescriptionThemeView(View):

    def get(self, request, id):

        theme = get_object_or_404(Theme, pk=id)
        return render(request, 'discussion/theme_description.html', context={'theme': theme})


class DiscussionRoomView(View):

    @method_decorator(login_required)
    def get(self, request, room_id):

        room = get_object_or_404(Room, pk=room_id)

        context = {
            'room': room,
        }

        return render(request, 'discussion/discussion.html', context)


class CreateDiscussionRoomView(View):

    @method_decorator(login_required)
    def get(self, request, theme_id):

        theme = Theme.objects.get(pk=theme_id)
        theme_current_rooms = Room.objects.filter(theme=theme)

        if theme_current_rooms.exists():
            last_current_room = theme_current_rooms.last()
            room_name = f'theme_{theme_id}_room_{last_current_room.id + 1}'
        else:
            room_name = f'theme_{theme_id}_room_1'

        room = Room.objects.create(name=room_name, theme=theme)
        RoomUser.objects.create(room=room, user=request.user)

        return redirect(reverse_lazy('discussion', kwargs={'room_id': room.pk}))
