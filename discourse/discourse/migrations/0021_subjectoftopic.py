# Generated by Django 3.1.2 on 2020-11-10 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0020_auto_20201109_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectOfTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_subject', models.CharField(max_length=100)),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discourse.topic')),
            ],
        ),
    ]