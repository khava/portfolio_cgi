import json
import os

from discussion.models import Bot, BotComment


def create_bot():

    data_path = os.path.join(os.path.dirname(__file__), 'data.json')

    bot_1, _ = Bot.objects.get_or_create(name='bot_1')
    bot_2, _ = Bot.objects.get_or_create(name='bot_2')

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for color in data:
        for comment in data[color]:
            BotComment.objects.get_or_create(comment=comment, color=color, bot=bot_1)
            BotComment.objects.get_or_create(comment=comment, color=color, bot=bot_2)
