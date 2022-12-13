# Generated by Django 4.1.2 on 2022-11-04 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeManagement', '0002_alter_employees_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending')], default='Pending', max_length=20, null=True),
        ),
    ]
