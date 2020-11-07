# Generated by Django 3.1.2 on 2020-11-07 11:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discourse', '0015_remove_topic_comment_of_author_of_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='topic',
            name='who_viewed',
            field=models.ManyToManyField(blank=True, related_name='who_viewed_t', to=settings.AUTH_USER_MODEL),
        ),
    ]
