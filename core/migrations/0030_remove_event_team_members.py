# Generated by Django 3.1.7 on 2021-04-05 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20210405_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='team_members',
        ),
    ]
