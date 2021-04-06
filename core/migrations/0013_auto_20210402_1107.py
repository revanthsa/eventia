# Generated by Django 3.1.7 on 2021-04-02 05:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_event_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
        migrations.AddField(
            model_name='event',
            name='team_members',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10)], verbose_name='team members'),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_name', models.CharField(help_text='team name must be unique', max_length=25, primary_key=True, serialize=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
            },
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'event'), name='unique_team'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'event', 'user'), name='unique_team_user'),
        ),
    ]
