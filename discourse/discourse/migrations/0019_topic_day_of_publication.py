# Generated by Django 3.1.2 on 2020-11-09 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0018_auto_20201109_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='day_of_publication',
            field=models.IntegerField(max_length=3, null=True),
        ),
    ]