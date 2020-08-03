from django import forms

from discussion.models import Topic


class CreateTopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ('topic', )