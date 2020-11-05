# Generated by Django 2.2.5 on 2020-10-28 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0004_auto_20201028_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomuser',
            name='bot',
        ),
        migrations.AddField(
            model_name='room',
            name='bots',
            field=models.ManyToManyField(related_name='rooms', to='discussion.Bot'),
        ),
    ]
