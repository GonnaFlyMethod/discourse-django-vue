# Generated by Django 3.1.2 on 2020-11-07 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0013_auto_20201106_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='topic',
            name='comment_of_author_of_topic',
            field=models.TextField(),
        ),
    ]