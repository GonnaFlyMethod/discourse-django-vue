# Generated by Django 3.1.2 on 2020-11-16 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0029_topic_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='self_url',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]