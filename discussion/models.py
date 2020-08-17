from django.db import models

from accounts.models import User


class Topic(models.Model):
    topic = models.TextField(verbose_name='topic')
    created_date = models.DateField(auto_now_add=True, verbose_name='created date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', related_name='topics')

    class Meta:
        ordering = ['-created_date', ]
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.topic


# class Room(models.Model):
#     name = models.CharField(max_length=255, verbose_name='room')
#     created_date = models.DateField(auto_now_add=True, verbose_name='created date')
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='topic', related_name='rooms')

#     class Meta:
#         verbose_name = 'Комната'
#         verbose_name_plural = 'Комнаты'

#     def __str__(self):
#         return name


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

    comment = models.TextField(verbose_name='comment')
    created_date = models.DateField(auto_now_add=True, verbose_name='created date')
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, verbose_name='color')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='topic', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', related_name='comments')
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='room', related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment
        