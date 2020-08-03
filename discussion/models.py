from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Topic(models.Model):
    topic = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic


class Comment(models.Model):

    WHITE = 'white'
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLACK = 'black'

    COLOR_CHOICES = (
        (WHITE, 'White'),
        (RED, 'Red'),
        (BLUE, 'Blue'),
        (GREEN, 'Green'),
        (YELLOW, 'Yellow'),
        (BLACK, 'Black')
    )

    comment = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    color = models.CharField(max_length=6, choices=COLOR_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment