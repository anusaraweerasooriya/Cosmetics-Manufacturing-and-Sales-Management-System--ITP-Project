# Generated by Django 4.1.2 on 2022-11-03 11:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerAndSalesManagement', '0005_alter_order_date_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 3, 17, 10, 47, 906838)),
        ),
    ]
