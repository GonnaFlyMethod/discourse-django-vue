# Generated by Django 3.1.2 on 2020-11-07 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0014_auto_20201107_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='comment_of_author_of_topic',
        ),
    ]
