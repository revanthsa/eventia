# Generated by Django 3.1.7 on 2021-04-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210402_1550'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='team',
            name='unique_team_user',
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'user'), name='unique_team_user1'),
        ),
    ]
