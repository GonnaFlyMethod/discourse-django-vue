# Generated by Django 3.1.2 on 2020-11-06 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0012_auto_20201106_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='short_description',
        ),
        migrations.AddField(
            model_name='topic',
            name='comment_of_author_of_topic',
            field=models.TextField(default=0, max_length=2000),
            preserve_default=False,
        ),
    ]
