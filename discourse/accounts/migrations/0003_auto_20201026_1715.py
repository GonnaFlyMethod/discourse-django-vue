# Generated by Django 3.1.2 on 2020-10-26 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201025_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='sex',
            field=models.CharField(max_length=20, verbose_name='Sex'),
        ),
    ]