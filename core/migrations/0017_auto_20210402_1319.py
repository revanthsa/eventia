# Generated by Django 3.1.7 on 2021-04-02 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210402_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='event',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.event'),
        ),
        migrations.AlterField(
            model_name='team',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
