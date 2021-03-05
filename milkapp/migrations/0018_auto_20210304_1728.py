# Generated by Django 3.1.5 on 2021-03-04 17:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('milkapp', '0017_auto_20210304_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboy',
            name='status',
            field=models.CharField(default='ACTIVE', max_length=50),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='timing',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]