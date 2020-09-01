from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from discussion.models import Theme, Comment
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

        return redirect(reverse('main'))

    
class DescriptionThemeView(View):

    def get(self, request, id):

        theme = Theme.objects.filter(pk=id).first()
        return render(request, 'discussion/theme_description.html', context={'theme': theme})


class DiscussionView(View):

    @method_decorator(login_required)
    def get(self, request, room_name):

        theme = Theme.objects.filter(pk=room_name).first()
        comments = Comment.objects.filter(theme=theme)

        context = {
            'theme': theme,
            'comments': comments
        }

        return render(request, 'discussion/discussion_room.html', context)
