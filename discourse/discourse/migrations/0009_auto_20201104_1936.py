# Generated by Django 3.1.2 on 2020-11-04 19:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discourse', '0008_auto_20201103_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='dislikes',
        ),
        migrations.AddField(
            model_name='comment',
            name='who_liked',
            field=models.ManyToManyField(related_name='accounts_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
