import FormulationAndLabManagement.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='equipments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_id', models.CharField(max_length=50, null=True, unique=True)),
                ('category', models.CharField(choices=[('Select Category', 'Select Category'), ('Test Tube', 'Test Tube'), ('Flask', 'Flask'), ('Beaker', 'Beaker'), ('Pipette', 'Pipette'), ('Burette', 'Burette'), ('Measuring Cylinder', 'Measuring Cylinder'), ('Laboratory Stand', 'Laboratory Stand'), ('Funnel', 'Funnel')], default='Select Category', max_length=100, null=True)),
                ('condition', models.CharField(choices=[('Choose Condition', 'Choose Condition'), ('Brand New', 'Brand New'), ('Used', 'Used'), ('Need Repair', 'Need Repair')], default='Choose Condition', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='harmfull_chemicals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chemical_name', models.CharField(max_length=200, null=True)),
                ('harmful_percentage', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_category', models.CharField(choices=[('Select Category', 'Select Category'), ('Skin Cosmetics', 'Skin Cosmetics'), ('Hair Cosmetics', 'Hair Cosmetics'), ('Nail Cosmetics', 'Nail Cosmetics'), ('Face Makeup', 'Face Makeup')], default='Select Category', max_length=100, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('preparation_method', models.TextField()),
                ('duration', models.DurationField(null=True)),
                ('product_image', models.ImageField(blank=True, default='default_image.jpg', null=True, upload_to='formulation/')),
            ],
        ),
        migrations.CreateModel(
            name='products_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_category', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('preparation_method', models.TextField()),
                ('duration', models.DurationField(null=True)),
                ('product_image', models.ImageField(blank=True, default='default_image.jpg', null=True, upload_to='formulation/')),
                ('action', models.CharField(max_length=20, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='schedule_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=200, null=True, unique=True)),
                ('method', models.CharField(max_length=5000, null=True)),
                ('status', models.CharField(choices=[('Select Status', 'Select Status'), ('Success', 'Success'), ('Unsuccess', 'Unsucsess'), ('Pending', 'Pending')], default='Select Status', max_length=100, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.products')),
            ],
        ),
        migrations.CreateModel(
            name='test_chemicals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chemical_name', models.CharField(max_length=200, null=True)),
                ('available_quantity', models.FloatField(null=True, validators=[FormulationAndLabManagement.models.test_chemicals.quantitity_validate])),
                ('status', models.CharField(choices=[('Select Status', 'Select Status'), ('Available', 'Available'), ('Not Available', 'Not Available')], default='Select Status', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='updated_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category', models.CharField(choices=[('Skin Cosmetics', 'Skin Cosmetics'), ('Hair Cosmetics', 'Hair Cosmetics'), ('Nail Cosmetics', 'Nail Cosmetics'), ('Face Makeup', 'Face Makeup')], max_length=100, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('preparation_method', models.CharField(max_length=5000, null=True)),
                ('duration', models.DurationField(null=True, validators=[FormulationAndLabManagement.models.updated_products.duaration_validate])),
                ('isSafe', models.CharField(max_length=100, null=True)),
                ('product_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.products')),
            ],
        ),
        migrations.CreateModel(
            name='schedule_test_chemicals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(null=True, validators=[FormulationAndLabManagement.models.schedule_test_chemicals.quantitity_validate])),
                ('chemical', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.test_chemicals')),
                ('test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.schedule_test')),
            ],
        ),
        migrations.CreateModel(
            name='lab_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateField(null=True)),
                ('test_result', models.CharField(max_length=500, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.products')),
            ],
        ),
        migrations.CreateModel(
            name='formulationhistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_material', models.CharField(max_length=1000, null=True)),
                ('formulation_qty', models.IntegerField(null=True)),
                ('action', models.CharField(max_length=20, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('product_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.products')),
            ],
        ),
        migrations.CreateModel(
            name='formulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_material', models.CharField(max_length=1000, null=True)),
                ('formulation_qty', models.FloatField(null=True)),
                ('product_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FormulationAndLabManagement.products')),
            ],
        ),
    ]
