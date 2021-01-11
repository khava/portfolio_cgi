# Generated by Django 2.2.15 on 2021-01-06 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0014_room_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='color_description',
            field=models.CharField(default='Управление, Информация и факты, Эмоции и Чувства, Критическое суждение, Оптимистичность, Креативность', max_length=101, verbose_name='color_description'),
        ),
        migrations.AddField(
            model_name='room',
            name='colors',
            field=models.CharField(default='blue, white, red, black, yellow, green', max_length=38, verbose_name='colors'),
        ),
    ]
