# Generated by Django 4.1.2 on 2022-11-04 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerAndSalesManagement', '0007_alter_order_date_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 14, 29, 7, 129850)),
        ),
    ]