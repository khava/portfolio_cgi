from django.contrib import admin

from discussion.models import BotComment, Bot, Comment, Room, RoomUser, RoomBot, Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('theme', 'created_date', 'author',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'created_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'color', 'theme', 'author', 'created_date', )


@admin.register(RoomUser)
class RoomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomBot)
class RoomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', )



@admin.register(BotComment)
class BotCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'color', 'bot', 'created_date', )
