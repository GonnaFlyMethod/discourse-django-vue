# Generated by Django 3.1.2 on 2020-11-10 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0022_auto_20201110_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagoftopic',
            name='name_of_subject',
        ),
        migrations.AddField(
            model_name='tagoftopic',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discourse.topic'),
        ),
        migrations.AlterField(
            model_name='tagoftopic',
            name='tag',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
