from django.contrib import admin

from discussion.models import Theme, Comment


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('theme', 'created_date', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'color', 'theme', 'author', 'created_date')
