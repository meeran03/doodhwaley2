# Generated by Django 3.1.5 on 2021-03-05 07:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('milkapp', '0019_deliveryboynotifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboynotifications',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
