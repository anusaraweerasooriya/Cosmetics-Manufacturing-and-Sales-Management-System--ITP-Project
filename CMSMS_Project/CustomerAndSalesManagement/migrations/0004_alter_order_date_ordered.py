# Generated by Django 4.1.2 on 2022-11-02 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerAndSalesManagement', '0003_alter_bulkorderrequest_province_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(),
        ),
    ]
