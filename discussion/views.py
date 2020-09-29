from datetime import datetime
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core import serializers

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


class DiscussionView(View):

    @method_decorator(login_required)
    def get(self, request, theme_id):

        users = []
        theme = get_object_or_404(Theme, pk=theme_id)
        room = Room.objects.filter(theme=theme).last()
        comments = Comment.objects.filter(theme=theme, room=room)

        if room is not None:
            users = User.objects.filter(rooms__name=room.name).order_by('roomuser__created_date')

        if request.is_ajax():

            if request.GET['last_user_name']:
                last_user_name = User.objects.get(username=request.GET['last_user_name'])
                user = User.objects.get(username=last_user_name)
                date = RoomUser.objects.get(room=room, user=user).created_date
                new_users = User.objects.filter(rooms__name=room.name, roomuser__created_date__gt=date)
                
                new_users_data = []
                for user in new_users:
                    new_users_data.append({'username': user.username, 'avatar': user.avatar.url})

                return HttpResponse(json.dumps(new_users_data))

            else:
                new_users_data = []
                for user in users:
                    new_users_data.append({'username': user.username, 'avatar': user.avatar.url})
                return HttpResponse(json.dumps(new_users_data))

        context = {
            'theme': theme,
            'users': users,
            'comments': comments,
        }

        return render(request, 'discussion/discussion_room.html', context)
