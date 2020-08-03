from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from discussion.models import Topic, Comment
from discussion.forms import CreateTopicForm


class DisplayTopicsView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'discussion/topic_list.html'


class CreateTopicView(CreateView):

    @method_decorator(login_required)
    def get(self, request):
        form = CreateTopicForm()
        return render(request, 'discussion/topic_create.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = CreateTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()

        return redirect(reverse('main'))


class DiscussionView(View):

    def get(self, request):
        return render(request, 'discussion/discussion_page.html')