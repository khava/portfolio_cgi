from django.contrib import admin

from discussion.models import Topic, Comment


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'created_date', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'color', 'topic', 'author', 'created_date')
