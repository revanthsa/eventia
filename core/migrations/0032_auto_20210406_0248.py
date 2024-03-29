# Generated by Django 3.1.7 on 2021-04-05 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_remove_winner_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='team',
            field=models.ForeignKey(help_text='If the winner is a group of participant, choose the team from here', on_delete=django.db.models.deletion.CASCADE, to='core.team'),
        ),
    ]
