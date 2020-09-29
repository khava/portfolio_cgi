from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from discussion.models import Theme, Room


class ThemesListView(View):

    @method_decorator(staff_member_required)
    def get(self, request):
        themes = Theme.objects.all()
        return render(request, 'moderator/themes_list.html', context={'themes': themes})
        

class ThemeDetailView(View):

    @method_decorator(staff_member_required)
    def get(self, request, theme_id):
        theme = get_object_or_404(Theme, pk=theme_id)
        return render(request, 'moderator/theme_detail.html', context={'theme': theme})


class ThemeDiscussionCommentsView(View):

    @method_decorator(staff_member_required)
    def get(self, request, theme_id, discussion_id):
        room = get_object_or_404(Room, theme=theme_id, pk=discussion_id)
        
        context = {
            'room': room,
            'red': room.comments.filter(color='red'),
            'blue': room.comments.filter(color='blue'),
            'yellow': room.comments.filter(color='yellow'),
            'green': room.comments.filter(color='green'),
            'white': room.comments.filter(color='white'),
            'black': room.comments.filter(color='black'),
        }
        return render(request, 'moderator/moderator_comments.html', context=context)


