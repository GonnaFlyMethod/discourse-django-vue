# Generated by Django 3.1.2 on 2020-11-21 17:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0032_topic_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
