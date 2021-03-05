# Generated by Django 3.1.5 on 2021-03-04 10:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('milkapp', '0016_auto_20210303_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_boy_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='user_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='timing',
            field=models.TimeField(default=datetime.time(10, 25, 40, 581864)),
        ),
    ]
