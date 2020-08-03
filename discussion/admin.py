from django.contrib import admin

from discussion.models import Topic, Comment


admin.site.register(Topic)
admin.site.register(Comment)
