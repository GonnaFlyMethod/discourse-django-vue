# Generated by Django 3.1.2 on 2020-11-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0030_auto_20201116_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='image_of_topic',
            field=models.ImageField(blank=True, null=True, upload_to='discourse/topic_images', verbose_name='Topic image'),
        ),
    ]
