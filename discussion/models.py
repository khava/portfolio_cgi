from itertools import chain

from django.db import models
from django.conf import settings

from accounts.models import User


class Theme(models.Model):
    theme = models.CharField(max_length=255, verbose_name='theme')
    problem = models.TextField(verbose_name='problem')
    decision = models.TextField(verbose_name='decision')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='created date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', related_name='themes')

    class Meta:
        ordering = ['-created_date', ]
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.theme


class Bot(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    avatar = models.ImageField(upload_to=settings.MEDIA_AVATAR_IMAGE_DIR, default='avatars/bot_avatar.jpg')

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    def __str__(self):
        return self.name

    
class BotComment(models.Model):

    COLOR_CHOICES = (
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('black', 'Black')
    )

    comment = models.TextField(verbose_name='comment')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='created date')
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, verbose_name='color')
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name='bot', related_name='comments')

    class Meta:
        verbose_name = 'Комментарии бота'
        verbose_name_plural = 'Комментарии ботов'

    def __str__(self):
        return self.comment


class Room(models.Model):

    COLORS = 'blue, white, red, black, yellow, green'
    COLOR_DESCRIPTION = 'Управление, Информация и факты, Эмоции и Чувства, Критическое суждение, Оптимистичность, Креативность'

    name = models.CharField(max_length=255, unique=True, verbose_name='name')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='created date')
    started = models.BooleanField(default=False, verbose_name='started')
    # started_time = models.DateTimeField(blank=True, null=True)
    closed = models.BooleanField(default=False, verbose_name='closed')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='theme', related_name='rooms')
    users = models.ManyToManyField(User, through='RoomUser', related_name='rooms')
    bots = models.ManyToManyField(Bot, through='RoomBot', blank=True, related_name='rooms')
    colors = models.CharField(max_length=38, default=COLORS, verbose_name='colors')
    color_description = models.CharField(max_length=101, default=COLOR_DESCRIPTION, verbose_name='color_description')

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.name

    def get_participants(self):
        return list(chain(self.users.order_by('roomuser__created_date'), self.bots.all()))

    def get_participants_count(self):
        return self.users.order_by('roomuser__5created_date').count() + self.bots.count()  


class RoomUser(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['room', 'user']]

    def __str__(self):
        return f'{self.room.name} - {self.user.username}'


class RoomBot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['room', 'bot']]

    def __str__(self):
        return f'{self.room.name} - {self.bot.name}'


class Comment(models.Model):

    COLOR_CHOICES = (
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('black', 'Black')
    )

    comment = models.TextField(verbose_name='comment')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='created date')
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, verbose_name='color')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='theme', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', related_name='comments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='room', related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment
           