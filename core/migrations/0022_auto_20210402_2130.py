# Generated by Django 3.1.7 on 2021-04-02 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_delete_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(help_text='team name must be unique', max_length=25)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
            },
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'event', 'user'), name='unique_team_event_user'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'event'), name='unique_team'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'user'), name='unique_team_user'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('event', 'user'), name='unique_event_user'),
        ),
    ]
