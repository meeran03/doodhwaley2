# Generated by Django 3.1.5 on 2021-02-28 08:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milkapp', '0004_auto_20210228_0759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='product',
            new_name='product_id',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='timing',
            field=models.TimeField(default=datetime.time(8, 1, 2, 631871)),
        ),
    ]