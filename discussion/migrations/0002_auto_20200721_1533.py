# Generated by Django 2.2.5 on 2020-07-21 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discussion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discussion.Color'),
        ),
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discussion.Topic'),
        ),
    ]
