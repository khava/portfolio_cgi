# Generated by Django 2.2.5 on 2020-08-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='theme',
            field=models.CharField(max_length=255, verbose_name='theme'),
        ),
    ]
